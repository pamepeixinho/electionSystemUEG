from numpy.distutils.fcompiler import none


class Voter(object):
    """
    ======
    Voter class
    ======
        Attributes:
            name: Name of voter
            cpf: Document (Required)
            photoUrl: Url of face photo of voter (Optional)
            votedFlag: if voter has vote in last election
            regionType: Enum :py:obj: ~UegProject.Model.Types.RegionType`
    """

    def __init__(self, name, cpf, voted_flag, region_type, photo_url=none):
        self.__name = name
        self.__cpf = cpf
        self.__photoUrl = photo_url
        self.__votedFlag = voted_flag
        self.__regionType = region_type