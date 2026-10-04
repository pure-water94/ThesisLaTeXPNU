# 부산대학교 나노메카트로닉스공학과 학위논문 LaTeX

이 포크는 [Isaac-Kwon/ThesisLaTeXPNU](https://github.com/Isaac-Kwon/ThesisLaTeXPNU)의 원본을 보존하고, **2026년 9월 부산대학교 학위논문 작성 준수사항**에 대응하는 국문 박사 수정판을 `nanomechatronics/`에 추가합니다.

- [사용 방법](nanomechatronics/README.md)
- [지침 대응표와 수용 기준](nanomechatronics/docs/compliance.md)
- [실제 빌드·검증 결과](nanomechatronics/docs/validation.md)
- [익명 예시 PDF](nanomechatronics/preview/example.pdf)

**학교가 발행하거나 승인한 공식 클래스는 아닙니다.** 개인의 학위종별·심사일·지도교수·위원은 자동 추론하지 않습니다. `draft`는 미확정값을 드러내고, `final`은 필수 메타데이터와 승인 플래그가 없으면 실패합니다. 원고의 학술적 진실성·표절·제출 자격까지 검증하는 도구는 아닙니다.

## 변경 범위

원본 `pnuthesis.cls`, `samples/`는 유지합니다. 새 프로필은 학과명 매개변수화, 표지 뒤 빈 면지, 인준지 간격, 표·그림목차, 양언어 초록, 자동 인용순 번호 및 검사 스크립트를 제공합니다. 기존 예제와 호환되지 않는 부분은 새 클래스에서만 바꿉니다.

공개 저장소에는 템플릿과 익명 예시만 있습니다. 실제 논문·개인정보는 `local-*` 파일에 두며 Git에서 제외합니다. `.gitignore`는 실수 방지 장치일 뿐, 커밋 전 내용 검토를 대신하지 않습니다.

## 출처·권리

기반 검토 커밋: `Isaac-Kwon/ThesisLaTeXPNU@29b215cfde83c7907674dc9d56d8945ae23fe929`.
원저장소의 출처와 기존 파일을 보존합니다. 원저장소에서 독립 LICENSE 파일은 확인되지 않았으므로 이 포크가 원본에 대해 새로운 무제한 재배포 권한을 부여한다고 해석하지 마세요. 학교 명칭은 서식 대상 식별을 위한 것입니다.
