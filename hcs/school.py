from .hcs import Route
from .models import SearchSchool

def searchSchool(lctnScCode: str, schulCrseScCode: str, orgName: str, loginType: str = "school"):
    response = Route("GET", "https://hcs.eduro.go.kr", f"/v2/searchSchool?lctnScCode={lctnScCode}&schulCrseScCode={schulCrseScCode}&orgName={orgName}&loginType={loginType}")
        
    if len(response.response.json()["schulList"]) > 1:
        raise IndexError("너무 많은 학교가 검색 되었습니다.")

    school = response.response.json()["schulList"][0]
    orgCode = school.get("orgCode")
    atptOfcdcConctUrl = school.get("atptOfcdcConctUrl")

    return SearchSchool(atptOfcdcConctUrl=atptOfcdcConctUrl, orgCode=orgCode)
