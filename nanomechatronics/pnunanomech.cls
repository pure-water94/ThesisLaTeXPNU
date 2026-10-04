% PNU 2026 Korean doctoral thesis profile for Nanomechatronics Engineering.
% Structural successor in this fork to Isaac-Kwon/ThesisLaTeXPNU (upstream
% 29b215cfde83c7907674dc9d56d8945ae23fe929). Upstream files are preserved.
% Not an official university class. See README and docs/compliance.md.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{pnunanomech}[2026/10/04 v0.1 PNU Korean doctoral profile]
\newif\ifpnufinal \pnufinalfalse
\DeclareOption{draft}{\pnufinalfalse}
\DeclareOption{final}{\pnufinaltrue}
\DeclareOption*{\ClassError{pnunanomech}{Unsupported option \CurrentOption}{Only draft and final are supported.}}
\ProcessOptions\relax
\RequirePackage{fix-cm}
\LoadClass[11pt,a4paper,oneside,onecolumn]{report}
\RequirePackage{fontspec}
\RequirePackage{kotex}
\RequirePackage{geometry}
\geometry{a4paper,left=25mm,right=25mm,top=35mm,bottom=25mm,headheight=0pt,headsep=0pt,footskip=15mm}
\RequirePackage{tikz}
\usetikzlibrary{positioning,calc}
\RequirePackage{setspace}
\RequirePackage{titlesec}
\RequirePackage{tocloft}
\RequirePackage{fancyhdr}
\RequirePackage{ragged2e}
\RequirePackage{indentfirst}
\RequirePackage{graphicx}
% Document draft metadata must not suppress raster figures.
\setkeys{Gin}{draft=false}
\RequirePackage{booktabs}
\RequirePackage{tabularx}
\RequirePackage{amsmath,amssymb}
\RequirePackage[numbers,sort&compress]{natbib}
\RequirePackage[font=small,labelfont=normalfont,labelsep=space]{caption}
\RequirePackage[final,unicode,hidelinks,bookmarksnumbered]{hyperref}
\RequirePackage{xfp}
% Portable default: TeX-distributed fonts, not copied proprietary font files.
% Body family is an editorial choice, not a mandatory PNU requirement.
\setmainfont{texgyretermes-regular.otf}[BoldFont=texgyretermes-bold.otf,ItalicFont=texgyretermes-italic.otf,BoldItalicFont=texgyretermes-bolditalic.otf]
\setmainhangulfont{UnBatang.ttf}[BoldFont=UnBatangBold.ttf,ItalicFont=UnBatang.ttf,ItalicFeatures={FakeSlant=0.15},BoldItalicFont=UnBatangBold.ttf,BoldItalicFeatures={FakeSlant=0.15}]
\InputIfFileExists{local-fonts.tex}{}{}
\newcommand{\PNUfont}[1]{\fontsize{#1bp}{\fpeval{#1*1.3}bp}\selectfont}
\renewcommand{\contentsname}{목차}
\renewcommand{\listtablename}{표목차}
\renewcommand{\listfigurename}{그림목차}
\renewcommand{\bibname}{참고문헌}
\renewcommand{\figurename}{그림}
\renewcommand{\tablename}{표}
\renewcommand{\appendixname}{부록}
\setcounter{tocdepth}{2}
\setcounter{secnumdepth}{2}
\titleformat{\chapter}[hang]{\sffamily\bfseries\PNUfont{16}}{제\thechapter 장}{1em}{}
\titleformat{\section}{\sffamily\bfseries\PNUfont{14}}{\thesection}{1em}{}
\titleformat{\subsection}{\sffamily\bfseries\PNUfont{12}}{\thesubsection}{1em}{}
\titlespacing*{\chapter}{0pt}{0pt}{18bp}
\titlespacing*{\section}{0pt}{12bp}{6bp}
\titlespacing*{\subsection}{0pt}{6bp}{3bp}
\setlength{\parindent}{5mm}
\setlength{\parskip}{5bp}
\setstretch{1.35}
% 1.35 times LaTeX baseline is NOT claimed equivalent to HWP 180%.
\setlength{\emergencystretch}{2em}
\clubpenalty=10000 \widowpenalty=10000
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\PNUfont{10}\thepage}\renewcommand{\headrulewidth}{0pt}\renewcommand{\footrulewidth}{0pt}}
\pagestyle{plain}
\renewcommand{\cfttoctitlefont}{\hfill\bfseries\PNUfont{15}}
\renewcommand{\cftaftertoctitle}{\hfill}
\renewcommand{\cftlottitlefont}{\hfill\bfseries\PNUfont{15}}
\renewcommand{\cftafterlottitle}{\hfill}
\renewcommand{\cftloftitlefont}{\hfill\bfseries\PNUfont{15}}
\renewcommand{\cftafterloftitle}{\hfill}
\setlength{\cftbeforetoctitleskip}{0pt}
\setlength{\cftbeforelottitleskip}{0pt}
\setlength{\cftbeforeloftitleskip}{0pt}
\newif\ifpnuapproved \pnuapprovedfalse
\newif\ifpnublank \pnublankfalse
\def\pnuTitleKo{} \def\pnuTitleEn{} \def\pnuAuthorKo{} \def\pnuAuthorEn{}
\def\pnuDegreeKo{} \def\pnuGraduation{} \def\pnuExamination{} \def\pnuAdviser{}
\def\pnuChair{} \def\pnuMemberA{} \def\pnuMemberB{} \def\pnuMemberC{} \def\pnuMemberD{}
\def\pnuDepartmentKo{나노메카트로닉스공학과}
\def\pnuDepartmentEn{Department of Nanomechatronics Engineering}
\def\pnuDraftLabel{검토용 초안 — 제출본 아님}
\pgfkeys{/pnu/.is family,/pnu,
 title-ko/.store in=\pnuTitleKo,title-en/.store in=\pnuTitleEn,
 author-ko/.store in=\pnuAuthorKo,author-en/.store in=\pnuAuthorEn,
 degree-ko/.store in=\pnuDegreeKo,graduation/.store in=\pnuGraduation,
 examination/.store in=\pnuExamination,adviser/.store in=\pnuAdviser,
 chair/.store in=\pnuChair,member-a/.store in=\pnuMemberA,member-b/.store in=\pnuMemberB,
 member-c/.store in=\pnuMemberC,member-d/.store in=\pnuMemberD,
 department-ko/.store in=\pnuDepartmentKo,department-en/.store in=\pnuDepartmentEn,
 draft-label/.store in=\pnuDraftLabel,approved/.is if=pnuapproved}
\newcommand{\PNUsetup}[1]{\pgfkeys{/pnu,#1}}
\newcommand{\PNUvalue}[2]{\ifx#1\@empty #2\else #1\fi}
\newcommand{\PNUrequire}[2]{\ifx#1\@empty\ClassError{pnunanomech}{Missing final metadata: #2}{Supply confirmed metadata; do not invent it.}\fi}
\AtBeginDocument{%
 \ifpnufinal
  \ifpnuapproved\else\ClassError{pnunanomech}{Final approval flag is false}{Use draft until all metadata and PDF layout are reviewed.}\fi
  \PNUrequire{\pnuTitleKo}{title-ko}\PNUrequire{\pnuTitleEn}{title-en}
  \PNUrequire{\pnuAuthorKo}{author-ko}\PNUrequire{\pnuAuthorEn}{author-en}
  \PNUrequire{\pnuDegreeKo}{degree-ko}\PNUrequire{\pnuGraduation}{graduation}
  \PNUrequire{\pnuExamination}{examination}\PNUrequire{\pnuAdviser}{adviser}
  \PNUrequire{\pnuChair}{chair}\PNUrequire{\pnuMemberA}{member-a}
  \PNUrequire{\pnuMemberB}{member-b}\PNUrequire{\pnuMemberC}{member-c}\PNUrequire{\pnuMemberD}{member-d}
 \fi
 \hypersetup{pdftitle={PNU Nanomechatronics Thesis},pdfauthor={}}
}
\AddToHook{shipout/background}{\ifpnufinal\else\ifpnublank\else
 \begin{tikzpicture}[remember picture,overlay]
 \node[anchor=north east,inner sep=0pt,font=\fontsize{8bp}{10bp}\selectfont,text=black!55] at ([xshift=-12mm,yshift=-10mm]current page.north east){\pnuDraftLabel};
 \end{tikzpicture}\fi\fi}
\tikzset{pnutext/.style={inner sep=0pt,outer sep=0pt,align=center,text width=160mm}}
% Layout measurement convention: zero-padding TeX text-box edges, not ink edges.
% This is documented implementation policy, NOT a university measurement rule.
\newcommand{\PNUMakeCover}{%
 \clearpage\pagenumbering{gobble}\thispagestyle{empty}\null
 \begin{tikzpicture}[remember picture,overlay]
 \node[pnutext,anchor=north,font=\PNUfont{16}] (degree) at ([yshift=-45mm]current page.north){박사학위논문};
 \node[pnutext,below=20mm of degree,font=\PNUfont{22}] (title){\PNUvalue{\pnuTitleKo}{논문 제목 입력}};
 \node[pnutext,anchor=south,font=\PNUfont{16}] (date) at ([yshift=40mm]current page.south){\PNUvalue{\pnuGraduation}{년\quad 월}};
 \node[pnutext,above=20mm of date,font=\PNUfont{16}] (dept){\pnuDepartmentKo};
 \node[pnutext,above=5mm of dept,font=\PNUfont{16}] (school){부산대학교 대학원};
 \node[pnutext,above=20mm of school,font=\PNUfont{16}] (author){\PNUvalue{\pnuAuthorKo}{성명 입력}};
 \path let \p1=(title.south),\p2=(author.north) in \pgfextra{\pgfmathsetlengthmacro{\pnugap}{\y1-\y2}\typeout{PNU-COVER-GAP=\pnugap}\ifdim\pnugap<5mm\ClassError{pnunanomech}{Cover title overlaps author area}{Shorten or explicitly reflow the title.}\fi};
 \end{tikzpicture}\clearpage}
\newcommand{\PNUMakeBlank}{\global\pnublanktrue\thispagestyle{empty}\null\clearpage\global\pnublankfalse}
\newcommand{\PNUCommitteeRow}[2]{\makebox[22mm][l]{#1}\makebox[78mm][l]{\PNUvalue{#2}{\underline{\hspace{50mm}}}}\makebox[10mm][r]{인}}
\newcommand{\PNUMakeApproval}{%
 \thispagestyle{empty}\null
 \begin{tikzpicture}[remember picture,overlay]
 \node[pnutext,anchor=north,font=\PNUfont{22}] (title) at ([yshift=-40mm]current page.north){\PNUvalue{\pnuTitleKo}{논문 제목 입력}};
 \node[pnutext,below=15mm of title,font=\PNUfont{16}] (submit){이 논문을 \PNUvalue{\pnuDegreeKo}{○○}박사 학위논문으로 제출함};
 \node[pnutext,below=10mm of submit,font=\PNUfont{14}] (author){\PNUvalue{\pnuAuthorKo}{성명 입력}};
 \node[pnutext,below=10mm of author,font=\PNUfont{14}] (school){부산대학교 대학원};
 \node[pnutext,below=5mm of school,font=\PNUfont{14}] (dept){\pnuDepartmentKo};
 \node[pnutext,below=10mm of dept,font=\PNUfont{14}] (adviser){지도교수\quad\PNUvalue{\pnuAdviser}{○ ○ ○}};
 \node[pnutext,anchor=south,font=\PNUfont{14}] (m4) at ([yshift=40mm]current page.south){\PNUCommitteeRow{위원}{\pnuMemberD}};
 \node[pnutext,above=5mm of m4,font=\PNUfont{14}] (m3){\PNUCommitteeRow{위원}{\pnuMemberC}};
 \node[pnutext,above=5mm of m3,font=\PNUfont{14}] (m2){\PNUCommitteeRow{위원}{\pnuMemberB}};
 \node[pnutext,above=5mm of m2,font=\PNUfont{14}] (m1){\PNUCommitteeRow{위원}{\pnuMemberA}};
 \node[pnutext,above=5mm of m1,font=\PNUfont{14}] (chair){\PNUCommitteeRow{위원장}{\pnuChair}};
 \node[pnutext,above=10mm of chair,font=\PNUfont{14}] (date){\PNUvalue{\pnuExamination}{년\quad 월\quad 일}};
 \node[pnutext,above=10mm of date,font=\PNUfont{16}] (approve){\PNUvalue{\pnuAuthorKo}{성명 입력}의 \PNUvalue{\pnuDegreeKo}{○○}박사 학위논문을 인준함};
 \path let \p1=(adviser.south),\p2=(approve.north) in \pgfextra{\pgfmathsetlengthmacro{\pnugap}{\y1-\y2}\typeout{PNU-APPROVAL-GAP=\pnugap}\ifdim\pnugap<5mm\ClassError{pnunanomech}{Approval title or metadata exceeds available space}{Reflow the title; do not overlap the approval block.}\fi};
 \end{tikzpicture}\clearpage}
\newcommand{\PNUMakeLists}{%
 \pagenumbering{Roman}\pagestyle{plain}
 \tableofcontents\clearpage
 \phantomsection\addcontentsline{toc}{chapter}{표목차}\listoftables\clearpage
 \phantomsection\addcontentsline{toc}{chapter}{그림목차}\listoffigures\clearpage}
\newcount\pnuabsstart
\newcommand{\PNUAbstract}[2]{%
 \clearpage\global\pnuabsstart=\value{page}\begingroup
 \setstretch{1}\setlength{\parskip}{0pt}\setlength{\parindent}{0pt}
 \def\pnuWhich{#1}\def\pnuKo{ko}
 \phantomsection
 \ifx\pnuWhich\pnuKo\addcontentsline{toc}{chapter}{국문초록}\else\addcontentsline{toc}{chapter}{Abstract}\fi
 \noindent\begin{tikzpicture}
 \ifx\pnuWhich\pnuKo
  \node[pnutext,anchor=north,font=\PNUfont{14}] (title) at (0,0){\PNUvalue{\pnuTitleKo}{논문 제목 입력}};
  \node[pnutext,below=15mm of title,font=\PNUfont{12}] (author){\PNUvalue{\pnuAuthorKo}{성명 입력}};
  \node[pnutext,below=10mm of author,font=\PNUfont{11}] (dept){부산대학교 대학원 \pnuDepartmentKo};
  \node[pnutext,below=15mm of dept,font=\PNUfont{12}] (label){요약};
 \else
  \node[pnutext,anchor=north,font=\PNUfont{14}] (title) at (0,0){\PNUvalue{\pnuTitleEn}{Thesis Title}};
  \node[pnutext,below=15mm of title,font=\PNUfont{12}] (author){\PNUvalue{\pnuAuthorEn}{Name}};
  \node[pnutext,below=10mm of author,font=\PNUfont{11}] (dept){\pnuDepartmentEn\\The Graduate School\\Pusan National University};
  \node[pnutext,below=15mm of dept,font=\PNUfont{12}] (label){Abstract};
 \fi
 \end{tikzpicture}\par\vspace{10mm}\nointerlineskip
 \setstretch{1.2}\PNUfont{11}\justifying\setlength{\parindent}{5mm}\setlength{\parskip}{0pt}
 #2\par
 \typeout{PNU-ABSTRACT-#1-PAGES=\the\numexpr\value{page}-\pnuabsstart+1\relax}
 \ifnum\numexpr\value{page}-\pnuabsstart+1\relax>2
  \ClassError{pnunanomech}{Abstract #1 exceeds two pages}{Shorten the abstract; do not shrink required font sizes.}
 \fi\endgroup\clearpage}
\newcommand{\PNUStartBody}{\clearpage\pagenumbering{arabic}\pagestyle{plain}\setstretch{1.35}\PNUfont{11}}
\renewcommand{\bibsection}{\chapter*{참고문헌}\phantomsection\addcontentsline{toc}{chapter}{참고문헌}}
\renewcommand{\bibfont}{\PNUfont{11}}
\setlength{\bibhang}{7mm}
\setlength{\bibsep}{3bp}
\newcommand{\PNUBibliography}[1]{\clearpage\bibliographystyle{unsrtnat}\bibliography{#1}\clearpage}
\newcommand{\PNUAppendix}{\clearpage\appendix\titleformat{\chapter}[hang]{\sffamily\bfseries\PNUfont{16}}{부록 \thechapter}{1em}{}}
\endinput
