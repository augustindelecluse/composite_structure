from checker.utils.dzn_utils import read_dzn_array, read_dzn
import re


class CSSolution:
    __sequences: list[list[int]]
    __indexes: list[list[int]]

    def __init__(self, path: str):
        self.path = path
        dzn_contents = read_dzn(self.path)
        self.__parse_dzn(dzn_contents)

    def __str__(self):
        """
        Returns a string representation of the CSSolution object.
        :return:
        """
        string = f"CSSolution(\n" + "\tsequences = [\n"
        for seq in self.__sequences:
            string += f"\t\t{seq},\n"
        string += "\t],\n\n" + "\tindexes = [\n"

        for idx in self.__indexes:
            string += f"\t\t{idx},\n"
        string += "\t]\n)"

        return string

    def __repr__(self):
        return self.__str__()

    def __parse_dzn(self, dzn_contents: dict) -> None:
        """

        :param dzn_contents:
        :return:
        """
        try:
            if 'seq' in dzn_contents:
                self.__parse_single_arrays(dzn_contents)
            else:
                self.__parse_multiple_arrays(dzn_contents)
        except KeyError:
            raise ValueError(f"Incorrect solution format.")

        self.__clean_data()

    def __clean_data(self) -> None:
        """

        :return:
        """
        self.__sequences = [[x for x in seq if x != 0] for seq in self.__sequences]
        self.__indexes = [[x - 1 for x in idx] for idx in self.__indexes]

    def __parse_single_arrays(self, dzn_contents: dict) -> None:
        """

        :param dzn_contents:
        :return:
        """
        T = re.findall(r"\|([^|]*)\|", dzn_contents['seq'])[0].count(",") + 1
        regex = r"\|" + ",".join([r"\d+"] * T)
        self.__sequences = read_dzn_array(
            dzn_contents['seq'],
            lambda x: list(map(int, x[1:].split(","))),
            regex
        )
        self.__indexes = read_dzn_array(
            dzn_contents['indexes'],
            lambda x: list(map(int, x[1:].split(","))),
            regex
        )

    def __parse_multiple_arrays(self, dzn_contents: dict) -> None:
        """

        :param dzn_contents:
        :return:
        """
        n = int(dzn_contents['n'])
        self.__sequences = []
        for node in range(n):
            self.__sequences.append(read_dzn_array(
                dzn_contents[f'seq{node}'],
                lambda x: int(x),
                r"\d+"
            ))

        m = int(dzn_contents['m'])
        self.__indexes = []
        for edge in range(m):
            self.__indexes.append(read_dzn_array(
                dzn_contents[f'idx{edge}'],
                lambda x: int(x),
                r"\d+"
            ))

    def sequences(self) -> list[list[int]]:
        """
        Returns the stacking sequences of the solution.
        :return: the stacking sequences of the solution.
        """
        return self.__sequences

    def indexes(self) -> list[list[int]]:
        """
        Returns the indexes of the solution.
        :return: the indexes of the solution.
        """
        return self.__indexes

    def thickness(self, idx):
        """
        Returns the thickness of the stacking sequence at index idx.
        :param idx: index of the stacking sequence.
        :return: the thickness of the stacking sequence at index idx.
        """
        return len(self.__sequences[idx]) if 0 <= idx < len(self.__sequences) else 0


if __name__ == '__main__':
    sol = CSSolution("../../local/test_sol.dzn")
    print(sol)
