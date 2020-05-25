# kakaoapy README

##### 박인영


## templates

### index.html

기본 버튼으로만 구성

(추후 카카오페이 UI 적용 예정)



### approval.html

카카오페이 결제 성공 시 보이는 화면



## views

### index

#### <POST일 경우 (카카오페이 결제 버튼을 눌렀을 때)>

- pip install requests 해야 함.

- requests.post로 카카오에 요청을 보낸다.
- headers에는 인증키(Admin Key)와 Content-type을 담아 보낸다.
- params에는 필수 파라미터들을 포함하여 보낸다.
- params 중에 url이 3개 있는데, 반드시 10~255자 이내로 구성되어야 한다. (상대 주소를 사용했다가 10자를 못넘어서 계속 오류가 났는데, 발견하고 고치는 데 오래 걸렸다.)

- res.text 프린트하면 딕셔너리 형태로 response가 찍히므로 확인할 수 있다.

