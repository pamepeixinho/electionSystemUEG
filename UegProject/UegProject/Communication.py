from django.http import HttpResponse
from django.http import JsonResponse

from UegProject.ErrorCodes import ErrorCodes
from UegProject.Model.Candidate import Candidate
from UegProject.Model.Region import Region
from UegProject.Model.Types.RoleType import RoleType
from UegProject.Model.Ueg import Ueg
from UegProject.Model.Voter import Voter
from UegProject.Model.Types.CommunicationType import CommunicationType as CT


class Communication(object):
    ueg = None

    @staticmethod
    def home(request):
        return HttpResponse('UEG')

    @staticmethod
    def __testingWithVotersArray():
        r = Region("Sao Paulo", "Sao Paulo", "Brasil")
        r2 = Region("Sao Bernardo do Campo", "Sao Paulo", "Brasil")
        vt1 = [Voter("Pamela", 123, False, r),
               Voter("Andre", 124, False, r),
               Voter("Ahmad", 125, False, r2),
               Voter("Marco", 126, False, r)]
        return vt1

    @staticmethod
    def __testingWithCandidatesArray():
        r = Region("Sao Paulo", "Sao Paulo", "Brasil")
        r2 = Region("Sao Bernardo do Campo", "Sao Paulo", "Brasil")
        vt2 = [Candidate("Pamela", 123, False, r, "url", 102, RoleType.DEPUTADO, "peixinho"),
               Candidate("Andre", 124, False, r, "url", 103, RoleType.PREFEITO, "dede"),
               Candidate("Ahmad", 125, False, r2, "url", 104, RoleType.PREFEITO, "mud"),
               Candidate("Marco", 126, False, r, "url", 105, RoleType.GOVERNADOR, "maco")]
        return vt2

    def sendData(self, request):
        if request.method != 'GET':
            return HttpResponse(ErrorCodes.WRONG_REQUEST)

        username = request.GET.get('username')
        password = request.GET.get('password')

        self.__verifyIfNew()

        # TODO call Authenticate
        authenticated = self.__authenticate(username, password, CT.CARREGAMENTO)
        if authenticated != True:
            return HttpResponse('ERRO {0}'.format(authenticated))

        uevJson = {
            # TODO get array BY UEG
            # "Eleitores": [v.toJSON() for v in self.ueg.getAllVoter()]
            # "Candidatos": [c.toJSON() for c in self.ueg.getAllCandidates()]
            "Eleitores": [v.toJSON() for v in self.__testingWithVotersArray()],
            "Candidatos": [c.toJSON() for c in self.__testingWithCandidatesArray()],
        }
        return JsonResponse(uevJson, safe=False)

    # TODO change function name
    # TODO verify requirement of this function and usage (Diagrams TOO)
    def __verifyIfNew(self):
        if self.ueg is None:
            self.ueg = Ueg()

    # TODO verify and update __authenticate usage in diagrams
    def __authenticate(self, username, password, communicationType):
        if self.ueg.isValidUev(username=username, password=password):
            if self.ueg.isValidElection(communicationType):
                return True
            else:
                return ErrorCodes.INVALID_TIME_ELECTION
        else:
            return ErrorCodes.INVALID_UEV
