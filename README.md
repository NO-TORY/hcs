# hcs
자가진단 자동화 라이브러리

# installation
```shell
pip install --upgrade py-hcs
```
# dependencies
[transkey](https://github.com/covid-hcs/transkey-py) <br/>
[hcs-python](https://github.com/covid-hcs/hcs-python)

# usage
```python
import hcs

hcs.selfcheck("김이름", "090103", "서울", "어딘가초등학교", "초등학교", "9328", True)
```

# tip
토큰으로 불러오면 더 빠르게 자가진단을 하실 수 있습니다! <br/>
```python
import hcs

hcs.token_selfcheck("토큰")
```