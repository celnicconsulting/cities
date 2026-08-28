# ====================ORG_BANNER====================
"""The hazard-striped provenance banner, shown above the tabs on every build.

The banner is fixed. The **only** thing that varies between platforms is the
sentence naming the agencies, which `agency_sentence()` builds.

Drawn as raw HTML rather than `st.warning` so the stripes survive both Streamlit
themes: a 3px black frame, a 14px yellow-and-black 45-degree stripe band top and
bottom, and a solid #FFD100 panel between them.

It sits **above the tabs, not in a footer**, so it is read before any figure
rather than found underneath one. These applications are built from public
releases but are not published by, nor endorsed by, the agencies that produced
them, and that has to be stated before the first number.

    render_provenance_banner([
        Agency("Ministry of Social Development", sub="StudyLink"),
        Agency("Ministry of Education"),
        Agency("the Treasury"),
        Agency("Kāinga Ora – Homes and Communities", article=False),
    ])

The article is the only subtlety, and it is a judgement about each agency's own
name rather than a rule a function can infer:

    Agency("Ministry of Education")               the <b>Ministry of Education</b>
    Agency("the Treasury")                        <b>the Treasury</b>
    Agency("Kāinga Ora", article=False)           <b>Kāinga Ora</b>

Default: "the " is prefixed outside the bold, because most agency names are
"Ministry of X" or "Department of Y". A name beginning "the "/"Te " is bolded
whole, because there the article belongs to the name. Set `article=False` for
names that take no article at all — Kāinga Ora, Stats NZ, Oranga Tamariki, Waka
Kotahi, Inland Revenue. Getting this wrong reads as carelessness about the
agencies being named, which is the opposite of what the banner is for.

Plain strings still work and follow the default rule, so
`["Ministry of Education", "the Treasury"]` needs no ceremony.
"""

from __future__ import annotations

import html
from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class Agency:
    """One agency named in the banner.

    `sub` is a second brand the agency publishes under that a reader will
    recognise — MSD and StudyLink. `article` is False for names that take no
    article.
    """

    name: str
    sub: str | None = None
    article: bool = True

STRIPE = "height:14px; background:repeating-linear-gradient(45deg, #FFD100 0 14px, #111 14px 28px);"


def _coerce(entry) -> Agency:
    if isinstance(entry, Agency):
        return entry
    if isinstance(entry, (tuple, list)):
        return Agency(entry[0], entry[1] if len(entry) > 1 else None)
    return Agency(str(entry))


def _render(a: Agency) -> str:
    escaped = html.escape(a.name)
    if not a.article or a.name.lower().startswith(("the ", "te ")):
        out = f"<b>{escaped}</b>"
    else:
        out = f"the <b>{escaped}</b>"
    if a.sub:
        out += f" (including <b>{html.escape(a.sub)}</b>)"
    return out


def agency_sentence(agencies) -> str:
    """The one varying fragment: the agencies whose releases the figures come from.

    A sub-brand is bolded too, because a reader scanning only the bold words
    should still see every body named.
    """
    parts = [_render(_coerce(e)) for e in agencies]
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " and " + parts[-1]


def render_provenance_banner(agencies, pipeline_tab: str = "&#9881;&#65039; Pipeline") -> None:
    """Hazard-striped provenance banner shown above every tab.

    `agencies` is passed to `agency_sentence`. `pipeline_tab` is the label of the
    tab that lists the source files, so the banner's final sentence points at
    something that actually exists — change it if the tab is renamed.
    """
    st.html(
        f"""
        <div style="border:3px solid #111; border-radius:6px; overflow:hidden;
                    margin:0 0 14px 0; font-family:sans-serif;">
          <div style="{STRIPE}"></div>
          <div style="background:#FFD100; color:#111; padding:12px 16px;">
            <div style="font-weight:800; font-size:15px; letter-spacing:.02em;">
              &#9888;&#65039; BUILT FROM NEW ZEALAND GOVERNMENT DATA &mdash;
              NOT AN OFFICIAL GOVERNMENT PRODUCT
            </div>
            <div style="font-size:13.5px; line-height:1.5; margin-top:6px;">
              Figures are reproduced from public releases by
              {agency_sentence(agencies)}.
              This application is produced independently by Celnic Consulting and
              <b>does not represent the views, policy or official statistics of those
              departments</b>. Every original source file, with its download date and
              checksum, is listed in the <b>{pipeline_tab}</b> tab.
            </div>
          </div>
          <div style="{STRIPE}"></div>
        </div>
        """
    )
