import re

from tagberry.epc.EPCFactory import EPCFactory
from tagberry.epcerrors.GS1Exception import GS1Exception

from tagberry.gs1 import GS1Factory
from tagberry.gs1 import sscc_patterns
from tagberry.utils.Utilities import isGS1


class EncodingFactory:
    def __init__(self):
        self.sscc_patterns = []
        for pat in sscc_patterns:
            self.sscc_patterns.append(re.compile(pat))

    def create(self, data):

        if isGS1(data):
            return GS1Factory()
        else:
            return EPCFactory()

    def parse(self, data, companyPrefix=None):
        retVal = None

        if isGS1(data):
            if companyPrefix is None:
                raise GS1Exception("In order to create a GS1 Encoding a company prefix is required")
            retVal = GS1Factory().parse(data, companyPrefix)
        else:
            retVal = EPCFactory().parse(data)

        return retVal
    
    def isSSCC(self, gs1):
        ret = False
        for pat in self.sscc_patterns:
            m = pat.match(gs1)
            if m is not None:
                ret = True
                break
        return ret
