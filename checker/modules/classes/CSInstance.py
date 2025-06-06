from checker.utils.dzn_utils import read_dzn_array, read_dzn


class CSInstance:
    __edges: list[tuple[int, int]]
    __counts: list[list[int]]

    def __init__(self, path: str):
        self.path = path
        dzn_contents = read_dzn(self.path)
        self.__parse_dzn(dzn_contents)

    def __str__(self):
        """
        Returns a string representation of the CSInstance object.
        :return:
        """
        return f"CSInstance(\n" \
            f"\tT = {self.T()},\n" \
            f"\tm = {self.m()},\n" \
            f"\tn = {self.n()},\n" \
            f"\tedges = {self.__edges},\n" \
            f"\tcounts = {self.__counts}\n" \
            f")"

    def __repr__(self):
        return self.__str__()

    def __parse_dzn(self, dzn_contents: dict) -> None:
        """

        :param dzn_contents:
        :return:
        """
        self.__edges = read_dzn_array(
            dzn_contents["edges"],
            lambda x: tuple(map(int, x[1:-1].split(","))),
            r"\(\d+,\d+\)"
        )
        self.__edges = [(parent - 1, child - 1) for parent, child in self.__edges]
        self.__counts = read_dzn_array(
            dzn_contents["counts"],
            lambda x: list(map(int, x[1:].split(","))),
            r"\|\d+,\d+,\d+,\d+"
        )

    def T(self):
        """
        Returns the thickness of the thickest stacking sequence in the instance.
        :return: the amount of plies in the thickest stacking sequence.
        """
        thicknesses = [sum(count) for count in self.__counts]
        return max(thicknesses) if thicknesses else 0

    def n(self):
        """
        Returns the number of counts in the instance.
        """
        return len(self.__counts)

    def m(self):
        """
        Returns the number of edges in the instance.
        """
        return len(self.__edges)

    def counts(self):
        """
        Returns the counts of the instance.
        :return: the number of plies for every angle that must be present in each stacking sequence.
        """
        return self.__counts

    def edges(self):
        """
        Returns the edges of the instance.
        :return: the edges of the instance
        """
        return self.__edges

    def thickness(self, inx):
        """
        Returns the thickness of the stacking sequence at index inx.
        :param inx: index of the stacking sequence.
        :return: the thickness of the stacking sequence at index inx.
        """
        if 0 <= inx < len(self.__counts):
            return sum(self.__counts[inx])
        return 0


if __name__ == '__main__':
    instance = CSInstance("../../instances/3x3/random_grid_bench_3_3_009.dzn")
    print(instance)
