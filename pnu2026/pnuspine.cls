% Standalone Korean doctoral printed-book spine, not an electronic thesis page.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{pnuspine}[2026/10/06 v0.1 Parameterized Korean spine]
\LoadClass{article}
\RequirePackage{fontspec,kotex,geometry,tikz}
\setmainfont{texgyretermes-regular.otf}
\setmainhangulfont{UnBatang.ttf}
\RequirePackage[unicode,hidelinks]{hyperref}
\hypersetup{pdftitle={Anonymous spine layout},pdfauthor={}}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\ExplSyntaxOn
\dim_new:N \l_pnus_width_dim
\dim_new:N \l_pnus_font_dim
\dim_new:N \l_pnus_titleheight_dim
\dim_new:N \l_pnus_step_dim
\clist_new:N \l_pnus_columns_clist
\tl_new:N \l_pnus_author_tl
\tl_new:N \l_pnus_date_tl
\box_new:N \l_pnus_author_box
\box_new:N \l_pnus_date_box
\box_new:N \l_pnus_title_box
\bool_new:N \g_pnus_made_bool
\keys_define:nn {pnuspine} {
 width .dim_set:N = \l_pnus_width_dim,
 font-size .dim_set:N = \l_pnus_font_dim,
 title-columns .clist_set:N = \l_pnus_columns_clist,
 author .tl_set:N = \l_pnus_author_tl,
 graduation .tl_set:N = \l_pnus_date_tl
}
\NewDocumentCommand\PNUspinesetup{m}{\keys_set:nn{pnuspine}{#1}}
\cs_new_protected:Npn \pnus_error:n #1 {
 \ClassError{pnuspine}{#1}{Supply~confirmed~binding~dimensions~and~metadata.~See~docs/spine.md.}
}
% Upright character cells; spaces are ignored. Braced tokens form one cell.
\cs_new_protected:Npn \pnus_cell:n #1 {
 \hbox to \l_pnus_step_dim{\hss\strut #1\hss}
}
\cs_new_protected:Npn \pnus_stack:n #1 {
 \vbox{\offinterlineskip\tl_map_inline:nn{#1}{\pnus_cell:n{##1}}}
}
\cs_generate_variant:Nn \pnus_stack:n {V}
\cs_new_protected:Npn \pnus_column:n #1 {
 \dim_compare:nNnT {\tl_count:n{#1}\l_pnus_step_dim} > {\l_pnus_titleheight_dim}
  {\pnus_error:n{Title~column~exceeds~available~height}}
 \vbox to \l_pnus_titleheight_dim{
  \offinterlineskip
  \int_zero:N \l_tmpa_int
  \tl_map_inline:nn{#1}{
   \int_compare:nNnT{\l_tmpa_int}>{0}{\vfil}
   \pnus_cell:n{##1}\int_incr:N\l_tmpa_int
  }
 }
}
\AtBeginDocument{
 \dim_compare:nNnF{\l_pnus_width_dim}>{0pt}{\pnus_error:n{Missing~positive~spine~width}}
 \dim_compare:nNnF{\l_pnus_font_dim}>{0pt}{\pnus_error:n{Missing~positive~spine~font-size}}
 \clist_if_empty:NT\l_pnus_columns_clist{\pnus_error:n{Missing~title-columns}}
 \tl_if_empty:NT\l_pnus_author_tl{\pnus_error:n{Missing~author}}
 \tl_if_empty:NT\l_pnus_date_tl{\pnus_error:n{Missing~graduation}}
}
% Configure in the preamble, then use this as the ONLY document content.
\NewDocumentCommand\PNUMakeSpine{}{
 \bool_if:NT\g_pnus_made_bool{\pnus_error:n{Spine~may~only~be~made~once}}
 \bool_gset_true:N\g_pnus_made_bool
 \fontsize{\l_pnus_font_dim}{1.3\l_pnus_font_dim}\selectfont
 \dim_set:Nn\l_pnus_step_dim{1.3\l_pnus_font_dim}
 \vbox_set:Nn\l_pnus_author_box{\pnus_stack:V\l_pnus_author_tl}
 \vbox_set:Nn\l_pnus_date_box{\pnus_stack:V\l_pnus_date_tl}
 \dim_set:Nn\l_pnus_titleheight_dim{
  297mm-40mm-20mm-\box_ht:N\l_pnus_author_box-\box_dp:N\l_pnus_author_box
  -\box_ht:N\l_pnus_date_box-\box_dp:N\l_pnus_date_box}
 \dim_compare:nNnF{\l_pnus_titleheight_dim}>{0pt}{\pnus_error:n{Name~and~date~exceed~available~height}}
 % Caller lists columns in reading order: rightmost first.
 \clist_reverse:N\l_pnus_columns_clist
 \hbox_set:Nn\l_pnus_title_box{
  \clist_map_inline:Nn\l_pnus_columns_clist{\pnus_column:n{##1}}
 }
 \dim_compare:nNnT{\box_wd:N\l_pnus_title_box}>{\l_pnus_width_dim-2mm}
  {\pnus_error:n{Spine~too~narrow~for~title~columns}}
 \dim_compare:nNnT{\l_pnus_step_dim}>{\l_pnus_width_dim-2mm}
  {\pnus_error:n{Spine~too~narrow~for~character~cell}}
 \iow_term:x{PNU-SPINE-WIDTH-PT=\dim_to_decimal:n{\l_pnus_width_dim}}
 \iow_term:x{PNU-SPINE-TITLE-HEIGHT-PT=\dim_to_decimal:n{\l_pnus_titleheight_dim}}
 \iow_term:x{PNU-SPINE-AUTHOR-HEIGHT-PT=\dim_to_decimal:n{\box_ht:N\l_pnus_author_box+\box_dp:N\l_pnus_author_box}}
 \iow_term:x{PNU-SPINE-DATE-HEIGHT-PT=\dim_to_decimal:n{\box_ht:N\l_pnus_date_box+\box_dp:N\l_pnus_date_box}}
 \thispagestyle{empty}\null
 \begin{tikzpicture}[remember~picture,overlay,every~node/.style={inner~sep=0pt,outer~sep=0pt}]
  \node[anchor=north] at ([yshift=-20mm]current~page.north){\box_use:N\l_pnus_title_box};
  \node[anchor=south] (date) at ([yshift=20mm]current~page.south){\box_use:N\l_pnus_date_box};
  \node[anchor=south] at ([yshift=10mm]date.north){\box_use:N\l_pnus_author_box};
 \end{tikzpicture}
}
\NewDocumentCommand\PNUspineGeometry{}{
 \geometry{paperwidth=\l_pnus_width_dim,paperheight=297mm,margin=0pt,headheight=0pt,headsep=0pt,footskip=0pt}
}
\ExplSyntaxOff
\endinput
