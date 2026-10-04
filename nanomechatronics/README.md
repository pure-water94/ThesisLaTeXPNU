# 나노메카트로닉스공학과 국문 박사 프로필

## 빠른 시작

검증 환경: Tectonic **0.17.0 Linux GNU** 배포, Python 3.12, PyMuPDF 1.28.2. Tectonic musl 빌드는 이 환경에서 ICU 한글 줄바꿈 오류를 보여 사용하지 않았습니다.

1. [Tectonic 공식 배포](https://github.com/tectonic-typesetting/tectonic/releases)에서 OS에 맞는 엔진을 설치합니다. 컴파일의 첫 실행은 TeX 패키지/글꼴을 내려받으므로 네트워크가 필요합니다. 엔진을 이 저장소에 포함하지 않습니다.
2. 이 디렉터리에서 실행합니다.

```sh
python build.py --tectonic /path/to/tectonic --test
python verify_pdf.py
```

`verify_pdf.py`는 PyMuPDF가 필요합니다. 격리 환경에서 `uv run --with pymupdf==1.28.2 python verify_pdf.py`로 실행할 수도 있습니다. 예시 PDF는 `build/example.pdf`, 빈 원고 시작본은 `build/main.pdf`입니다. 검사 중 의도한 음성시험의 exit code 1은 정상적인 차단 성공입니다.

### 개인 원고 시작

`metadata.example.tex`를 **local-metadata.tex**로 복사해 확정된 값만 채웁니다. 다음 개인 파일은 Git에서 제외됩니다.

- `local-metadata.tex`: 제목·성명·학위종별·지도교수·학위수여일·실제 최종심사일·위원.
- `local-abstract-ko.tex`, `local-abstract-en.tex`: 실제 초록. 각각 2쪽 이내.
- `local-body.tex`: 실제 본문. `\chapter`, `\section`, `\subsection` 사용.
- `local-references.bib`: 실제로 인용한 문헌의 검증된 서지정보.
- `local-appendix.tex`: 부록이 있는 경우에만 추가.
- `local-fonts.tex`: 필요한 경우 개인 글꼴 설정. 글꼴 파일은 공개 저장소에 올리지 않습니다.

```sh
python build.py --tectonic /path/to/tectonic --input main.tex
```

국문 학과명은 **나노메카트로닉스공학과**, 영문은 **Department of Nanomechatronics Engineering**으로 기본 설정합니다. 학과명으로 학위종별을 추정하지 않으며, 날짜를 현재 날짜로 자동 입력하지 않습니다. 긴 제목은 의미 단위에 맞춰 `\\`로 줄을 나누고 다시 검수할 수 있습니다.

### 제출 모드

확정되지 않은 값이 하나라도 있으면 계속 `draft`로 작업합니다. 모든 필수값과 실제 원고 파일을 준비하고 사람이 확인한 후 `local-metadata.tex`에서 `approved=true`를 설정합니다.

```sh
python build.py --tectonic /path/to/tectonic --final
```

결과는 `build/release-main.pdf`입니다. 승인 플래그는 **작성자의 확인 표시**이며 학교의 제출승인·논문통과를 뜻하지 않습니다. 이름이 들어 있다는 것만으로 그 값이 사실인지 도구가 알 수 없으므로, 실제 학적정보와 대조해야 합니다. 최종 PDF 전체 재검수·학교 제출 체크리스트 확인은 별도입니다.

## 구성과 인용

`main.tex`는 표지 → 번호 없는 백지 → 속표지/인준 → 목차·표목차·그림목차 → 국문초록 → 본문 → 참고문헌 → 선택 부록 → 영문초록 순서입니다. 표와 그림이 없으면 해당 목록 호출을 명시적으로 제거하고 목차·페이지를 다시 검사하세요.

- 인용: `\citep{key}`. natbib + BibTeX `unsrtnat`로 **첫 인용 순서**에 따라 번호가 부여됩니다. `.bib` 파일의 나열 순서와 다릅니다.
- 그림: `\caption` 뒤에 `\label`, 본문에서 `\ref`/`\pageref`.
- 표: `\caption`은 위, 그림은 아래에 둡니다. 예시 참조.
- 샘플 문헌은 공개 서지정보를 이용한 번호 시험용입니다. 실제 원고에 그대로 끼워 넣지 마세요.
- 본문 영문 제목 표기·참고문헌 분야별 스타일은 지도교수 기준으로 확정합니다. 이 프로필의 numeric/unsrtnat는 학교 강제 양식이 아닙니다.

## 서식 선택과 제한

본문 기본 글꼴은 TeX 배포의 UnBatang/UnDotum 및 TeX Gyre Termes입니다. 학교가 지정한 유일한 본문 글꼴이라고 주장하지 않습니다. 글꼴 변경 후 표지/인준/초록의 실측과 전체 페이지 재검사가 필요합니다.

`setstretch`는 LaTeX baseline 배율이며 HWP 180%와 동등하지 않습니다. 필수 표지·인준·초록 글자 크기는 PDF point(1/72 inch)에 맞춰 bp 단위로 지정했습니다. 도식 간격은 TeX 텍스트상자 경계 기준으로 구현하고, PDF 잉크경계 측정도 함께 보존합니다. 공식 도식은 측정 기준을 따로 정의하지 않으므로 모든 잉크경계가 정확히 동일한 cm라고 주장하지 않습니다.

현재 대상은 **국문 박사**입니다. 영문 본문·석사·양면 제본 프로필과 편집 가능한 HWP 변환은 검증하지 않았습니다. PDF와 HWP를 동시에 정본으로 수작업 편집하지 말고 공통 원고/서지 데이터를 관리하세요.

`--untrusted`로 컴파일하며 shell escape를 사용하지 않습니다. 실제 연구자료는 공개 원격 저장소에 업로드하지 않습니다.
