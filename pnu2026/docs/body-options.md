# 선택형 본문 기능

모든 선택은 지도교수와 협의하는 본문 편집 방식이며 학교 필수 규정이 아니다. 기존 `pnuthesis2026.cls`의 기본 동작은 바꾸지 않는다.

```tex
\usepackage[chapter-references,section-newpage,center-large-objects]{pnuoptions}
```

원하는 옵션만 지정한다. 아무 옵션 없이 로드하면 절 새 페이지, 큰 도표 중앙 페이지, 장별 참고문헌은 모두 꺼져 있다.

## 장별 참고문헌

`chapter-references`는 natbib + chapterbib을 사용한다. 각 장을 `\include{local-chapter-a}`처럼 불러오고 그 장 끝에 `\PNUChapterBibliography{local-references}`를 넣는다. 각 장에서 실제 인용한 항목만 그 장의 참고문헌에 나오며 번호는 장마다 다시 시작한다. 같은 키를 다른 장에서 다시 인용할 수 있다. 이 모드에서는 기본의 전체 `\PNUBibliography`를 함께 호출하지 않는다.

```sh
python build.py --tectonic /path/to/tectonic --input body-options-example.tex --chapter-bib
# 실제 원고도 같은 방식, 확정/검수 후에는 --final --chapter-bib 조합 가능
```

Tectonic 0.17.0은 chapterbib의 하위 AUX를 자동으로 BibTeX 처리하지 않았다. `--chapter-bib`는 1차 컴파일 후 각 장 AUX의 실제 인용·스타일·DB를 읽고, 임시 TeX 드라이버를 통해 **실제 내장 BibTeX를 실행**한 뒤 장별 BBL을 넣어 재컴파일한다. 가짜 참고문헌이나 직접 합성한 BBL을 사용하지 않는다. 임시 드라이버/BBL은 정상·오류 종료 시 정리하고 기존 BBL은 덮어쓰지 않는다. 동시 빌드는 피한다. 강제 프로세스 종료 시 남은 임시파일은 확인 후 제거한다.

지원 범위는 프로젝트 안의 상대경로 `\include` + BibTeX/natbib이다. biblatex/Biber, 파일명에 매크로를 쓰는 특수 구성, 이미 있는 수동 BBL과의 혼합은 검증하지 않았다. 장 사이를 건너뛰는 문헌 인용이 필요하면 전체 참고문헌 모드를 사용한다. 합성 시험용 `.bib`의 2099/2098년 자료는 **소프트웨어 시험 전용 허구 서지**이며 실제 연구문헌이 아니다.

## 절 새 페이지

`section-newpage`: 각 장의 **첫 절은 장 제목과 함께** 둔다. 이후 `\section`은 새 페이지를 시작한다. 별표형과 짧은 목차 제목 옵션을 보존한다. subsection에는 강제 새 페이지를 적용하지 않는다. 연속된 별표형 제목은 numbered section 카운터에 기반하므로 원하는 위치에서 직접 `\clearpage`를 사용할 수 있다.

## 큰 도표 중앙 페이지

```tex
\begin{PNUObject}{figure}
\centering
% generated figure or user-owned image
\caption{Caption}\label{fig:sample}
\end{PNUObject}
```

`table`도 가능하며 표 캡션은 위에 둔다. 개체 상자 높이가 본문 높이의 55%를 넘으면 독립 페이지의 **본문 영역 중앙**에 놓는다. 55%는 구현상 편집 기준이지 공식 규정이 아니다. 작으면 일반 float를 사용한다. 개체를 확대·축소하거나 분할하지 않으며 본문 높이 초과는 오류로 차단한다. `longtable`, 페이지를 넘기는 표, 내부 float, 개체 내부 footnote는 이 단일 상자 환경에 넣지 않는다.

## 제목 유지와 영문 각주

- 제목 바로 앞에 `\PNUKeepHeading[6\baselineskip]`처럼 공간을 예약한다. 기본은 5줄 높이이며 필요한 제목+본문 높이를 작성자가 지정한다. 긴 문단 전체를 자동으로 한 페이지에 묶는 명령은 아니다.
- `\PNUEnglishFootnote{English text}`는 기존 각주 번호 체계를 유지하면서 본문 로마체로 영문을 배치한다. 기울임은 `\emph{...}`로 지정한다. 별도의 번역·언어추론·글꼴 파일 복사 기능은 없다.

## 검증 재현

```sh
python build.py --tectonic /path/to/tectonic --test
uv run --with pymupdf==1.28.2 python verify_pdf.py
uv run --with pymupdf==1.28.2 python verify_options.py
```

`--untrusted`로 shell escape 없이 컴파일한다. `docs/reports/extended-test-results.json`은 확장된 양성/음성 시험, `baseline-regression.json`은 기존 예시 회귀검사, `options-validation.json`은 신규 PDF 측정 결과다. 보고서의 해시는 그 실행의 `build` 출력에 대한 것으로 생성 시각이 다르면 PDF 해시가 달라질 수 있다. `preview/body-options-example.pdf`와 `preview/spine-example.pdf`는 신규 기능의 익명 실출력이다.
