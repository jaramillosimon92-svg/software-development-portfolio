"""Presentation-only pieces for the editing workspace."""

from __future__ import annotations

import html

import streamlit as st


STYLE = """
<style>
:root { --studio-violet:#9b6dff; --studio-lilac:#c4a8ff; }
[data-testid="stMainBlockContainer"] { max-width:1320px; padding-top:1.2rem; padding-bottom:6rem; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap:.75rem; }
[data-testid="stSidebar"] { border-right:1px solid rgba(155,109,255,.16); }
[data-testid="stSidebar"] button { border-radius:10px; }
[data-testid="stMain"] h1,[data-testid="stMain"] h2,[data-testid="stMain"] h3 { letter-spacing:-.045em; }
.studio-shell.landing { min-height:calc(100svh - 7rem); display:flex; flex-direction:column; justify-content:center; }
.studio-hero { position:relative; isolation:isolate; overflow:hidden; min-height:380px; margin-bottom:1rem; padding:clamp(28px,4.4vw,64px); border:1px solid #292037; border-radius:24px; color:#f5f0ff; background:radial-gradient(ellipse at 80% 42%,rgba(98,53,179,.25),transparent 32%),linear-gradient(122deg,#100d19 0%,#151020 55%,#0b0a12 100%); display:grid; grid-template-columns:minmax(0,1.35fr) minmax(245px,.65fr); align-items:center; }
.studio-hero:before { content:""; position:absolute; inset:0; pointer-events:none; opacity:.35; background-image:linear-gradient(90deg,rgba(190,163,245,.10) 1px,transparent 1px); background-size:25% 100%; }
.studio-hero:after { content:""; position:absolute; width:520px; height:520px; right:-225px; top:-270px; border-radius:50%; border:1px solid rgba(188,150,255,.13); box-shadow:0 0 0 70px rgba(164,111,255,.025),0 0 0 140px rgba(164,111,255,.02); pointer-events:none; }
.studio-copy { position:relative; z-index:2; }
.studio-topline { display:flex; align-items:center; gap:12px; margin-bottom:30px; color:#b7a2d9; text-transform:uppercase; letter-spacing:.23em; font:600 .67rem/1.5 ui-monospace,SFMono-Regular,monospace; }
.studio-topline:before { content:""; width:22px; height:1px; background:var(--studio-violet); }
.studio-title { max-width:820px; margin:0; color:#faf7ff; font-size:clamp(3.8rem,7vw,7rem); line-height:.95; letter-spacing:-.083em; font-weight:800; }
.studio-tagline { margin:17px 0 0; color:#faf7ff; font-size:clamp(1.75rem,3.2vw,3rem); line-height:1.08; letter-spacing:-.055em; font-weight:700; }
.studio-tagline em { color:var(--studio-lilac); font-style:normal; }
.studio-description { max-width:480px; margin:27px 0 0; color:#b9b2c7; font-size:.96rem; line-height:1.75; }
.studio-hero-foot { display:flex; align-items:center; gap:12px; margin-top:35px; color:#afa3be; font:500 .68rem/1.5 ui-monospace,SFMono-Regular,monospace; text-transform:uppercase; letter-spacing:.12em; }
.studio-hero-foot:before { content:""; width:33px; height:1px; background:#a274f5; }
.studio-art { position:relative; z-index:1; height:290px; display:grid; place-items:center; }
.studio-player { width:min(100%,318px); padding:18px 20px 16px; border:1px solid rgba(185,144,255,.34); border-radius:23px; background:linear-gradient(145deg,rgba(52,34,82,.9),rgba(24,17,38,.94)); box-shadow:0 25px 65px rgba(9,4,20,.48),inset 0 1px rgba(232,210,255,.12); transform:rotate(-5deg); animation:studio-float 5s ease-in-out infinite; }
.studio-player-head,.studio-player-footer { display:flex; align-items:center; justify-content:space-between; color:#c2a9e9; font:600 .61rem ui-monospace,SFMono-Regular,monospace; letter-spacing:.16em; text-transform:uppercase; }
.studio-player-head span:first-child { display:flex; align-items:center; gap:8px; }
.studio-player-head span:first-child:before { content:""; width:7px; height:7px; border-radius:50%; background:#bc92ff; box-shadow:0 0 13px #a273f1; }
.studio-player-body { position:relative; height:160px; display:grid; place-items:center; }
.studio-player-disc { position:absolute; width:138px; aspect-ratio:1; border-radius:50%; background:repeating-radial-gradient(circle at center,transparent 0 7px,rgba(219,191,255,.16) 8px 9px),radial-gradient(circle at 35% 26%,#9a61ef,#512b89 54%,#1c122d 78%); border:1px solid rgba(225,200,255,.34); box-shadow:0 0 0 13px rgba(174,111,255,.055),0 13px 30px rgba(7,2,18,.34); animation:studio-turn 8s linear infinite; }
.studio-player-disc:after { content:""; position:absolute; width:28px; aspect-ratio:1; inset:50% auto auto 50%; translate:-50% -50%; border-radius:50%; background:#e5d4ff; border:7px solid #7b4bbc; box-shadow:0 0 0 2px rgba(28,12,51,.5); }
.studio-player-play { z-index:1; position:absolute; width:48px; aspect-ratio:1; display:grid; place-items:center; border-radius:50%; background:rgba(19,10,37,.9); border:1px solid rgba(239,221,255,.6); box-shadow:0 0 24px rgba(181,125,255,.45); }
.studio-player-play:after { content:""; width:0; height:0; margin-left:4px; border-top:8px solid transparent; border-bottom:8px solid transparent; border-left:12px solid #f7efff; }
.studio-player-wave { position:absolute; right:0; bottom:20px; display:flex; gap:4px; align-items:center; height:42px; }
.studio-player-wave span { width:3px; height:var(--bar); border-radius:3px; background:linear-gradient(#e1c7ff,#9c65f2); transform-origin:center; animation:studio-beat 1s ease-in-out infinite alternate; animation-delay:var(--delay); }
.studio-player-progress { height:3px; overflow:hidden; border-radius:4px; background:rgba(205,168,255,.22); }
.studio-player-progress:after { content:""; display:block; width:38%; height:100%; border-radius:4px; background:#c096ff; box-shadow:0 0 12px #b780ff; animation:studio-progress 9s linear infinite alternate; }
.studio-player-footer { margin-top:11px; color:#9484a9; letter-spacing:.1em; }
.studio-steps { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; margin:0 0 2.4rem; }
.studio-step { min-width:0; display:flex; align-items:center; gap:14px; padding:18px 20px; border:1px solid rgba(150,126,180,.18); border-radius:12px; background:rgba(126,87,173,.045); transition:border-color .2s ease,background .2s ease,transform .2s ease; }
.studio-step b { color:#867a96; font:600 .7rem ui-monospace,SFMono-Regular,monospace; }
.studio-step strong { min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:.83rem; font-weight:600; }
.studio-step.active { border-color:rgba(155,109,255,.58); background:rgba(125,72,224,.12); }
.studio-step.active b { color:#c4a8ff; }
.studio-section-head { display:flex; align-items:end; justify-content:space-between; gap:1rem; margin:2.5rem 0 1.35rem; padding:0 0 1.15rem; border-bottom:1px solid rgba(146,122,175,.22); }
.studio-section-head small { color:#ab81ff; font:600 .68rem ui-monospace,SFMono-Regular,monospace; text-transform:uppercase; letter-spacing:.16em; }
.studio-section-head h2 { margin:.5rem 0 0; font-size:clamp(2rem,3.4vw,3.25rem); line-height:1; letter-spacing:-.065em; }
.studio-section-head p { max-width:420px; margin:0; color:#a39bad; font-size:.88rem; line-height:1.55; text-align:right; }
[class*="st-key-scene_card_"] { border-radius:14px; transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease; }
[class*="st-key-scene_card_"]:hover { transform:translateY(-3px); box-shadow:0 14px 32px rgba(14,5,33,.18); border-color:rgba(155,109,255,.58); }
[class*="st-key-scene_card_"] img { border-radius:8px; }
[data-testid="stMain"] button { transition:transform .2s ease,box-shadow .2s ease; }
[data-testid="stMain"] button:hover { transform:translateY(-2px); box-shadow:0 9px 24px rgba(70,34,132,.2); }
[data-testid="stMain"] [data-testid="stVideo"] { border-radius:14px; overflow:hidden; }
@keyframes studio-turn { to { transform:rotate(360deg); } }
@keyframes studio-float { 50% { transform:translateY(-8px) rotate(-3deg); } }
@keyframes studio-beat { to { transform:scaleY(.42); opacity:.62; } }
@keyframes studio-progress { to { width:78%; } }
@keyframes studio-reveal { from { opacity:.55; transform:translateY(18px); } to { opacity:1; transform:translateY(0); } }
@supports (animation-timeline:view()) { .studio-section-head,[class*="st-key-scene_card_"] { animation:studio-reveal both; animation-timeline:view(); animation-range:entry 0% entry 55%; } }
@media (max-width:850px) { .studio-hero { grid-template-columns:1fr; min-height:350px; } .studio-art { position:absolute; width:260px; height:260px; right:-55px; bottom:-30px; opacity:.3; } .studio-description { max-width:70%; } }
@media (max-width:650px) { [data-testid="stMainBlockContainer"] { padding-top:.7rem; } .studio-shell.landing { min-height:auto; } .studio-hero { min-height:365px; padding:28px; border-radius:17px; } .studio-title { font-size:clamp(3.2rem,13vw,5rem); } .studio-tagline { font-size:clamp(1.6rem,6vw,2.2rem); } .studio-description { max-width:100%; } .studio-art { opacity:.13; right:-90px; } .studio-steps { gap:6px; } .studio-step { padding:11px 8px; gap:4px; flex-direction:column; text-align:center; } .studio-step strong { font-size:.66rem; } .studio-section-head { display:block; } .studio-section-head p { margin-top:.65rem; text-align:left; } }
@media (prefers-reduced-motion:reduce) { .studio-player,.studio-player-disc,.studio-player-wave span,.studio-player-progress:after,.studio-section-head,[class*="st-key-scene_card_"] { animation:none!important; } *,*:before,*:after { scroll-behavior:auto!important; transition-duration:.01ms!important; } }
</style>
"""


def render_hero(stage: int) -> None:
    shell_class = "studio-shell landing" if stage == 1 else "studio-shell"
    steps = (("01", "Source & beat"), ("02", "Choose scenes"), ("03", "Review & export"))
    step_markup = "".join(
        f'<div class="studio-step {"active" if index == stage else ""}"><b>{number}</b><strong>{name}</strong></div>'
        for index, (number, name) in enumerate(steps, 1)
    )
    wave = "".join(
        f'<span style="--bar:{height}px;--delay:{index * -.11:.2f}s"></span>'
        for index, height in enumerate((11, 22, 35, 17, 29, 39, 21, 32, 14))
    )
    st.html(STYLE)
    st.html(f"""
      <div class="{shell_class}">
      <div class="studio-hero">
        <div class="studio-copy">
          <div class="studio-topline">Music video / Creative workspace</div>
          <h1 class="studio-title">Syncora</h1>
          <p class="studio-tagline">Cut to <em>the feeling.</em></p>
          <p class="studio-description">Turn your favorite moments into a beat-synced video. Choose the scenes, shape the pace, and make the final cut yours.</p>
          <div class="studio-hero-foot">Your sound. Your vision.</div>
        </div>
        <div class="studio-art" aria-hidden="true">
          <div class="studio-player">
            <div class="studio-player-head"><span>Now playing</span><span>01 / 01</span></div>
            <div class="studio-player-body">
              <div class="studio-player-disc"></div><div class="studio-player-play"></div>
              <div class="studio-player-wave">{wave}</div>
            </div>
            <div class="studio-player-progress"></div>
            <div class="studio-player-footer"><span>Sound in motion</span><span>Syncora</span></div>
          </div>
        </div>
      </div>
      <div class="studio-steps" aria-label="Editing progress">{step_markup}</div>
      </div>
    """)


def section_heading(number: str, title: str, description: str) -> None:
    st.html(
        f'<div class="studio-section-head"><div><small>{html.escape(number)}</small>'
        f'<h2>{html.escape(title)}</h2></div><p>{html.escape(description)}</p></div>'
    )
