from .hcs import Route

class SearchSchool:
    def __init__(self, lctnScCode: str, schulCrseScCode: str, orgName: str, loginType: str = "school"):
        response = Route("GET", "https://hcs.eduro.go.kr", f"/v2/searchSchool?lctnScCode={lctnScCode}&schulCrseScCode={schulCrseScCode}&orgName={orgName}&loginType={loginType}")
        
        if len(response.response.json()["schulList"]) > 1:
            raise IndexError("너무 많은 학교가 검색 되었습니다.")

        self.school = response.response.json()["schulList"][0]
        self.orgCode = self.school.get("orgCode")
        self.atptOfcdcConctUrl = self.school.get("atptOfcdcConctUrl")