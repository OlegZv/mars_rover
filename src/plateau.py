from .rover import MarsRover, OutOfPlateauError, CollisionError
from math import pi
import logging as log


class Plateau(object):
    """
    The class of the plateau to where the rovers will be deployed.
    The class can be extended providing different characteristics like gravity or terrain
    """

    def __init__(self):
        "The plateau is initializes with list of rovers on it"
        self.rovers = {}

    def deploy_rover(self, rover_id, rover):
        """Method to deply a rover on the plateau

        Parameters
        ----------
        rover : Rover
            A instance of a Rover type/subtype that is deployed

        rover_id : str
            A unique ID of the rover deployed on the plateau
        """
        self.rovers[rover_id] = rover

    def is_in_range(self, x, y):
        """Method to check if the position in a range of the plateu"""
        pass

    def is_position_available(self):
        """Method to check if the collision will occur"""
        pass


class Mars(Plateau):
    """Class that describes Mars plateau

    Raises
    ------
    OutOfPlateauError
        The error is raised when the initial location is out of the plateau range
    CollisionError
        The error is raised when the location of a rover is not available. e.g. taken by other rover
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        super().__init__()

    @classmethod
    def from_string(cls, input_data):
        """The method will parse the input_data from a string

        Parameters
        ----------
        input_data : str
            a string that defines x and y upper-right coordinates of the plateau, divided by a space
        """
        try:
            x, y = list(map(int, input_data.split(" ")))
        except ValueError:
            log.error("The plateau initialization command is incorrect: {}".format(input_data))
            raise
        return cls(x, y)

    def deploy_rover(self, instructions, rover_id=None):
        """Method to deploy the rover on the plateau

        Parameters
        ----------
        instructions : str
            Describes Mars plateau specific instructions of the deployment in the format of "X Y D"
            Where X and Y are coordinates of the deployemnt and D is an initial direction of the rover

        rover_id : str optional
            Defines the ID of the rover. If not defined will be generated by default

        Returns
        -------
        MarsRover
            the rover that was deployed

        Raises
        ------
        OutOfPlateauError
            The error is raised when the initial location is out of the plateau range
        CollisionError
            The error is raised when the location of a rover is not available. e.g. taken by other rover
        """
        # unpack the initial location
        instructions = instructions.upper().split(" ")
        x, y = int(instructions[0]), int(instructions[1])
        if not self.is_in_range(x, y):
            raise OutOfPlateauError("The initial location of a rover is outside of range")
        if not self.is_position_available(x, y):
            raise CollisionError("the initial location of a rover is not available")
        if rover_id is None:
            # for now just length of the existing dict + 1. Guarantees to be unique
            rover_id = str(len(self.rovers) + 1)
        # convert direction from a letter to radians
        conver_direction = {"N": pi / 2, "S": -pi / 2, "E": 0, "W": pi}
        new_rover = MarsRover(rover_id, x, y, conver_direction[instructions[2]], self)
        # deploy defined rover on the plateau
        super().deploy_rover(rover_id, new_rover)
        return new_rover

    def is_in_range(self, x, y):
        """method checks if the x an y are in range of a plateau

        Parameters
        ----------
        x : int
            X coordinate to check
        y : int
            Y coordinate to check

        Returns
        -------
        bool
            If True - the x and y are in range of a plateau, False otherwise
        """
        if not 0 <= x <= self.x or not 0 <= y <= self.y:
            return False
        return True

    def is_position_available(self, x, y):
        """Method to check if the move to the x,y coordinates may collide with another rover

        Parameters
        ----------
        x : int
            X coordinate to check
        y : int
            Y coordinate to check

        Returns
        -------
        bool
            If True - the x and y position is available, False otherwise
        """
        for rover in self.rovers.values():
            if rover.get_location() == (x, y):
                return False
        return True
