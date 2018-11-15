class ProjectData:
    projects=[{"id":"0","name":"xwiki","package":"xwiki"},
                {"id":"1","name":"chart","package":"chart"},
                {"id":"2","name":"lang","package":"lang3"},
                {"id":"3","name":"math","package":"math3"},
                {"id":"4","name":"mockito","package":"mockito"},
                {"id":"5","name":"time","package":"time"},
                {"id":"6","name":"es","package":"elasticsearch"}
              ]
    def findProject(self,id):
        result = {}
        for p in self.projects:
            if p["id"] == id:
                result = p
                break
        return result
class CaseData:
    cases = [
        {"id": "10", "project": "0", "name": "XWIKI-13031", "version": "7.4", "fixed": "1", "fixed_version": "7.4.1",
         "buggy_frame": "2"},
        {"id": "4", "project": "0", "name": "XWIKI-13916", "version": "8.4", "fixed": "1", "fixed_version": "8.4.2",
         "buggy_frame": "1"},
        {"id": "17", "project": "0", "name": "XWIKI-13196", "version": "7.4.2", "fixed": "0", "fixed_version": "",
         "buggy_frame": ""}
             ]



class OtherData:
    p_functional_mocking = [0.8]
    functional_mocking_percent = [0.5]
    search_budget = [62328]
    population = [100]
    seed_clone=[0]
    seed_mutations=[0]
    p_object_pool=[0]
    # First index: target probability  |  Second index: non-target probability
    p_model_pool_init = [[0.2, 0.2]];
    repeat = 1
