# 기여 가이드

> **English:** Please open an issue before sending a pull request for anything non-trivial. Run `claude plugin validate . --strict` before you push, and never commit real personal data (résumés, contacts, tokens).

기여를 환영합니다. 중요한 변경은 풀 리퀘스트 전에 [이슈](https://github.com/seonwooj0810/careerloop/issues)를 먼저 열어 주세요.

## 변경 전후 확인

1. 수정한 뒤 레포 루트에서 `claude plugin validate . --strict`를 실행해 `✔ Validation passed`를 확인합니다.
2. `claude --plugin-dir .`로 플러그인을 불러와 바뀐 스킬을 직접 실행해 봅니다. 데이터가 필요하면 가상 인물의 이력서로 만든 임시 폴더를 쓰세요.
3. 스킬이나 에이전트를 고쳤다면 `plugin.json`의 `version`을 올립니다. 버전이 같으면 사용자가 업데이트를 받지 못합니다.

## 지켜야 할 원칙

- **사실만 씁니다.** 이력서와 프로필에 없는 경력·성과를 만들어 쓰지 않고, 공백은 공백으로 보고합니다.
- **경력 연수는 날짜로 계산합니다.** 표기와 계산값이 다르면 계산값을 쓰고 불일치를 알립니다.
- **개인정보를 커밋하지 않습니다.** 실제 이력서, 연락처, 토큰, 면접 전사본은 올리지 마세요.
- 커밋 메시지는 한국어 Conventional Commits(`fix(skill): …`)를 씁니다.

## 라이선스

기여한 내용은 이 레포의 [Apache License 2.0](LICENSE)을 따릅니다.
