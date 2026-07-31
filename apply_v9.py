#!/usr/bin/env python3
"""Apply v9 changes to index.html"""
import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

changes = 0

# ===== 1. OSTA layout: reduce grid to 1/3 width =====
old = ".osta-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;height:calc(100vh - 200px);min-height:400px}"
new = ".osta-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;height:auto;min-height:280px;max-width:360px;margin:0 auto}"
html = html.replace(old, new)
changes += 1

# Shrink OSTA blocks
old = ".osta-start .osta-icon{font-size:56px;margin-bottom:10px}"
new = ".osta-start .osta-icon{font-size:40px;margin-bottom:6px}"
html = html.replace(old, new)
changes += 1

old = ".osta-start .osta-label{font-size:20px;font-weight:700}"
new = ".osta-start .osta-label{font-size:16px;font-weight:700}"
html = html.replace(old, new)
changes += 1

old = ".osta-start .osta-sub{font-size:12px;opacity:.8;margin-top:4px}"
new = ".osta-start .osta-sub{font-size:10px;opacity:.8;margin-top:2px}"
html = html.replace(old, new)
changes += 1

old = ".osta-wrong .osta-icon{font-size:36px;margin-bottom:6px}"
new = ".osta-wrong .osta-icon{font-size:28px;margin-bottom:4px}"
html = html.replace(old, new)
changes += 1

old = ".osta-wrong .osta-label{font-size:15px;font-weight:600}"
new = ".osta-wrong .osta-label{font-size:13px;font-weight:600}"
html = html.replace(old, new)
changes += 1

old = ".osta-bank .osta-icon{font-size:36px;margin-bottom:6px}"
new = ".osta-bank .osta-icon{font-size:28px;margin-bottom:4px}"
html = html.replace(old, new)
changes += 1

old = ".osta-bank .osta-label{font-size:15px;font-weight:600}"
new = ".osta-bank .osta-label{font-size:13px;font-weight:600}"
html = html.replace(old, new)
changes += 1

old = "}.osta-badge-count{position:absolute;top:10px;right:10px;"
new = "}.osta-badge-count{position:absolute;top:8px;right:8px;"
html = html.replace(old, new)
changes += 1

# ===== 2. Add refresh icon style (Apple-style) =====
refresh_css = """.refresh-icon-btn{width:32px;height:32px;border-radius:16px;border:none;background:rgba(0,0,0,.05);display:inline-flex;align-items:center;justify-content:center;cursor:pointer;font-size:16px;transition:all .15s;flex-shrink:0;color:var(--accent)}
.refresh-icon-btn:active{background:rgba(0,0,0,.12);transform:scale(.92)}
.refresh-icon-btn svg{width:16px;height:16px}"""
if "refresh-icon-btn" not in html:
    # Insert after the last CSS style before </style>
    html = html.replace("</style>", refresh_css + "\n</style>")
    changes += 1

# ===== 3. Version bump to v9 =====
html = html.replace("style=\"font-size:9px;color:#c7c7cc;margin-left:4px\">v8", "style=\"font-size:9px;color:#c7c7cc;margin-left:4px\">v9")
html = html.replace('.register(\'./sw.js?v=8\')', '.register(\'./sw.js?v=9\')')
html = html.replace('src="osta.js?v=8"', 'src="osta.js?v=9"')
changes += 1

# ===== 4. English: add refresh button in renderEnglish =====
old_en_header = '<div style="font-size:14px;font-weight:600;margin-bottom:10px">\uD83D\uDDE3\uFE0F \u6BCF\u65E5\u82F1\u8BED\u7EC3\u4E60 <span style="font-size:11px;color:var(--text2);font-weight:400">(30\u5929\u53BB\u91CD \u00B7 3\u7BC7)</span></div>'
new_en_header = '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px"><div style="font-size:14px;font-weight:600">\uD83D\uDDE3\uFE0F \u6BCF\u65E5\u82F1\u8BED\u7EC3\u4E60 <span style="font-size:11px;color:var(--text2);font-weight:400">(30\u5929\u53BB\u91CD \u00B7 3\u7BC7)</span></div><button class="refresh-icon-btn" onclick="refreshEnIcon(this)" title="\u5237\u65B0\u7D20\u6750"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M1 4v6h6"/><path d="M3.5 16A9 9 0 005 10.5 9 9 0 0119 13"/><path d="M23 20v-6h-6"/><path d="M20.5 8A9 9 0 0019 13.5 9 9 0 015 11"/></svg></button></div>'

# Find renderEnglish function and modify it
# The renderEnglish header starts after "function renderEnglish(area){"
old_func = 'function renderEnglish(area){\n  var passages=pickEnPassages();_enPassages=passages;\n  var h=\'<div style="font-size:14px;font-weight:600;margin-bottom:10px">'
if old_func in html:
    new_func = 'function renderEnglish(area){\n  var passages=pickEnPassages();_enPassages=passages;\n  var h=\'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px"><div style="font-size:14px;font-weight:600">'
    html = html.replace(old_func, new_func)
    # Now fix the closing of the first h string
    # The pattern is: ...(30天去重 · 3篇)</span></div>\';
    old_close = '\u00B7 3\u7BC7)</span></div>\';'
    if old_close in html:
        # We need to be more careful. Let's find the exact pattern.
        pass

# Use a specific regex approach for renderEnglish
# The current pattern (after partial replacement above):
# ...font-weight:600">🗣️ 每日英语练习...
# Let me find the exact pattern using a more targeted approach

# Actually, let me find the exact anchor text
# After the partial replacement, the first div in renderEnglish starts with:
# <div style="font-size:14px;font-weight:600">

# I need to find the EXACT old string to replace
# Let me search for the pattern more carefully

en_pattern = '<div style="font-size:14px;font-weight:600;margin-bottom:10px">\uD83D\uDDE3\uFE0F \u6BCF\u65E5\u82F1\u8BED\u7EC3\u4E60 <span style="font-size:11px;color:var(--text2);font-weight:400">(30\u5929\u53BB\u91CD \u00B7 3\u7BC7)</span></div>'

# Check if this still exists in the file
if en_pattern in html:
    en_replacement = '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px"><div style="font-size:14px;font-weight:600">\uD83D\uDDE3\uFE0F \u6BCF\u65E5\u82F1\u8BED\u7EC3\u4E60 <span style="font-size:11px;color:var(--text2);font-weight:400">(30\u5929\u53BB\u91CD \u00B7 3\u7BC7)</span></div><button class="refresh-icon-btn" onclick="refreshEnIcon(this)" title="\u5237\u65B0\u7D20\u6750"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M1 4v6h6"/><path d="M3.5 16A9 9 0 005 10.5 9 9 0 0119 13"/><path d="M23 20v-6h-6"/><path d="M20.5 8A9 9 0 0019 13.5 9 9 0 015 11"/></svg></button></div>'
    html = html.replace(en_pattern, en_replacement)
    changes += 1
    print("English header replaced successfully")
else:
    print("WARNING: English header pattern not found")

# ===== 5. Add refreshEnIcon function =====
# Find the refreshEn function and add refreshEnIcon before it
old_refresh_en = "function refreshEn(){var es=getEnState();"
new_refresh_icon = "function refreshEnIcon(btn){if(btn){btn.style.animation='spin .6s ease';setTimeout(function(){btn.style.animation=''},600)}refreshEn();}\nfunction refreshEn(){var es=getEnState();"
if old_refresh_en in html:
    html = html.replace(old_refresh_en, new_refresh_icon)
    changes += 1
    print("refreshEnIcon added")

# Add spin animation to CSS
spin_css = "@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}"
if "keyframes spin" not in html:
    html = html.replace("</style>", spin_css + "\n</style>")
    changes += 1

# ===== 6. Video module: remove analysis from cards, fix refresh button =====
# Current video card pattern in renderVideoCards:
# '<div class="video-card"><div class="video-player-inline">...<div class="video-info"><h4>'+v.title+'</h4><div class="video-stat">...<div style="font-size:12px...💡 '+v.analysis+'</div></div></div>'

# Remove the analysis line from video cards
old_video_card = '<div class="video-card"><div class="video-player-inline"><iframe src="\'+v.embedUrl+\'" style="width:100%;height:200px;border:none" allow="autoplay;encrypted-media" allowfullscreen loading="lazy"></iframe></div><div class="video-info"><h4>\'+v.title+\'</h4><div class="video-stat">\'+v.platform+\' \u00B7 \'+v.author+\' \u00B7 \U0001f441 \'+v.views+\' \u00B7 \u2764 \'+v.likes+\'</div><div style="font-size:12px;line-height:1.5;color:var(--text2);margin-top:4px">\U0001f4a1 \'+v.analysis+\'</div></div></div>'
new_video_card = '<div class="video-card"><div class="video-player-inline"><iframe src="\'+v.embedUrl+\'" style="width:100%;height:200px;border:none" allow="autoplay;encrypted-media" allowfullscreen loading="lazy"></iframe></div><div class="video-info"><h4>\'+v.title+\'</h4><div class="video-stat">\'+v.platform+\' \u00B7 \'+v.author+\' \u00B7 \U0001f441 \'+v.views+\' \u00B7 \u2764 \'+v.likes+\'</div></div></div>'
if old_video_card in html:
    html = html.replace(old_video_card, new_video_card)
    changes += 1
    print("Video analysis removed from cards")
else:
    print("WARNING: Video card pattern not found")

# Replace video refresh button with Apple-style icon
old_vid_refresh = '<button class="btn btn-outline btn-sm" onclick="refreshVideos()">\U0001f504 \u5237\u65b0\u89c6\u9891</button>'
new_vid_refresh = '<button class="refresh-icon-btn" onclick="refreshVideosIcon(this)" title="\u5237\u65b0\u89c6\u9891"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M1 4v6h6"/><path d="M3.5 16A9 9 0 005 10.5 9 9 0 0119 13"/><path d="M23 20v-6h-6"/><path d="M20.5 8A9 9 0 0019 13.5 9 9 0 015 11"/></svg></button>'
if old_vid_refresh in html:
    html = html.replace(old_vid_refresh, new_vid_refresh)
    changes += 1
    print("Video refresh button replaced")

# Add refreshVideosIcon function
old_refresh_vid = "function refreshVideos(){var vs=getVideoState();"
new_refresh_vid_func = "function refreshVideosIcon(btn){if(btn){btn.style.animation='spin .6s ease';setTimeout(function(){btn.style.animation=''},600)}refreshVideos();}\nfunction refreshVideos(){var vs=getVideoState();"
if old_refresh_vid in html:
    html = html.replace(old_refresh_vid, new_refresh_vid_func)
    changes += 1

# ===== 7. Fitness module: 2-tab layout + 2-column cards =====
# Current renderFitness creates:
# 1. Card with 今日运动记录 + input form
# 2. Card with 上传跟练动作 + preview
# 3. customExList (已上传跟练动作)

# New structure: tab bar with 2 tabs + conditional content
# Tab 1: 今日运动记录 (show log + input form)
# Tab 2: 已上传跟练动作 (show upload form + card list)

old_fitness = """function renderFitness(area){
  var st=ld('fitness',{exercises:[],custom:[]});var t=td();var log=st.exercises.filter(function(e){return e.date===t});
  area.innerHTML='<div class="card"><div class="card-title">\U0001f4aa \u4ECA\u65E5\u8FD0\u52A8\u8BB0\u5F55 <span style="font-size:11px;color:var(--text2);font-weight:400">\u2190 \u5DE6\u6ED1\u5220\u9664</span></div>'+
    (log.length>0?'<div style="background:rgba(52,199,89,.08);border-radius:var(--radius-sm);padding:10px;margin-bottom:8px"><span style="font-size:13px;color:var(--success);font-weight:600">\u2705 \u5DF2\u6253\u5361 \u00B7 \u5171 '+log.reduce(function(s,e){return s+e.duration},0)+'\u5206\u949F</span></div>':'')+
    '<div id="todayExList">'+renderExList(log)+'</div>'+
    '<div style="display:flex;gap:8px;margin-top:10px"><input class="input" placeholder="\u8FD0\u52A8\u540D\u79F0" id="exName" style="flex:1"><input class="input" placeholder="\u5206\u949F" id="exDuration" style="width:70px;text-align:center" type="number" value="15"></div>'+
    '<button class="btn btn-primary btn-block" style="margin-top:8px" onclick="logEx()">\u2795 \u6DFB\u52A0\u8FD0\u52A8</button></div>'+
    '<div class="card"><div class="card-title">\U0001f4e4 \u4E0A\u4F20\u8DDF\u7EC3\u52A8\u4F5C</div>'+
    '<input class="input" placeholder="\u52A8\u4F5C\u540D\u79F0\uFF08\u5FC5\u586B\uFF09" id="customExName" style="margin-bottom:8px"><br>'+
    '<textarea class="input textarea" placeholder="\u52A8\u4F5C\u63CF\u8FF0/\u8981\u70B9\uFF08\u9009\u586B\uFF09" id="customExDesc" style="min-height:60px;margin-bottom:8px"></textarea><br>'+
    '<div style="display:flex;gap:8px;margin-bottom:8px"><button class="btn btn-outline" onclick="uploadExPhoto()">\U0001f4f8 \u62CD\u6444</button><button class="btn btn-outline" onclick="selectExPhoto()">\U0001f5bc\uFE0F \u9009\u7167\u7247</button></div>'+
    '<img id="exPhotoPreview" class="upload-preview" style="display:none">'+
    '<button class="btn btn-primary btn-block" onclick="saveEx()">\U0001f4be \u4FDD\u5B58\u52A8\u4F5C</button></div>'+
    '<div style="margin-top:12px" id="customExList">'+renderCustomExList(st.custom)+'</div>';
  // Bind swipe events
  bindSwipeEvents();
}"""

new_fitness = """function renderFitness(area){
  var st=ld('fitness',{exercises:[],custom:[]});var t=td();var log=st.exercises.filter(function(e){return e.date===t});
  area.innerHTML='<div class="tab-bar" style="margin-bottom:12px"><button class="tab-item active" onclick="switchFTab(\'today\',this)">\U0001f4aa \u4ECA\u65E5\u8FD0\u52A8\u8BB0\u5F55</button><button class="tab-item" onclick="switchFTab(\'uploaded\',this)">\U0001f4e4 \u5DF2\u4E0A\u4F20\u8DDF\u7EC3\u52A8\u4F5C</button></div><div id="fitnessContent"></div>';
  renderFTabContent('today',log,st);
  window._fitnessLog=log;window._fitnessSt=st;
}
function switchFTab(tab,btn){
  document.querySelectorAll('#contentArea .tab-item').forEach(function(t){t.classList.remove('active')});
  btn.classList.add('active');
  var log=window._fitnessLog;var st=window._fitnessSt;
  renderFTabContent(tab,log||[],st||ld('fitness',{exercises:[],custom:[]}));
}
function renderFTabContent(tab,log,st){
  var el=document.getElementById('fitnessContent');if(!el)return;
  if(tab==='today'){
    el.innerHTML='<div class="card"><div class="card-title">\U0001f4aa \u4ECA\u65E5\u8FD0\u52A8\u8BB0\u5F55 <span style="font-size:11px;color:var(--text2);font-weight:400">\u2190 \u5DE6\u6ED1\u5220\u9664</span></div>'+
      (log.length>0?'<div style="background:rgba(52,199,89,.08);border-radius:var(--radius-sm);padding:10px;margin-bottom:8px"><span style="font-size:13px;color:var(--success);font-weight:600">\u2705 \u5DF2\u6253\u5361 \u00B7 \u5171 '+log.reduce(function(s,e){return s+e.duration},0)+'\u5206\u949F</span></div>':'')+
      '<div id="todayExList">'+renderExList(log)+'</div>'+
      '<div style="display:flex;gap:8px;margin-top:10px"><input class="input" placeholder="\u8FD0\u52A8\u540D\u79F0" id="exName" style="flex:1"><input class="input" placeholder="\u5206\u949F" id="exDuration" style="width:70px;text-align:center" type="number" value="15"></div>'+
      '<button class="btn btn-primary btn-block" style="margin-top:8px" onclick="logEx()">\u2795 \u6DFB\u52A0\u8FD0\u52A8</button></div>';
    bindSwipeEvents();
  }else{
    el.innerHTML='<div class="card"><div class="card-title">\U0001f4e4 \u4E0A\u4F20\u8DDF\u7EC3\u52A8\u4F5C</div>'+
      '<input class="input" placeholder="\u52A8\u4F5C\u540D\u79F0\uFF08\u5FC5\u586B\uFF09" id="customExName" style="margin-bottom:8px"><br>'+
      '<textarea class="input textarea" placeholder="\u52A8\u4F5C\u63CF\u8FF0/\u8981\u70B9\uFF08\u9009\u586B\uFF09" id="customExDesc" style="min-height:60px;margin-bottom:8px"></textarea><br>'+
      '<div style="display:flex;gap:8px;margin-bottom:8px"><button class="btn btn-outline" onclick="uploadExPhoto()">\U0001f4f8 \u62CD\u6444</button><button class="btn btn-outline" onclick="selectExPhoto()">\U0001f5bc\uFE0F \u9009\u7167\u7247</button></div>'+
      '<img id="exPhotoPreview" class="upload-preview" style="display:none">'+
      '<button class="btn btn-primary btn-block" onclick="saveEx()">\U0001f4be \u4FDD\u5B58\u52A8\u4F5C</button></div>'+
      '<div style="margin-top:12px" id="customExList">'+renderCustomExList2(st.custom)+'</div>';
  }
}"""

if old_fitness in html:
    html = html.replace(old_fitness, new_fitness)
    changes += 1
    print("Fitness module restructured")

# Add renderCustomExList2 with 2-column grid
old_custom_ex = """function renderCustomExList(cl){
  if(!cl||cl.length===0)return'<div class="empty-state"><div class="empty-icon">\U0001f4f7</div><p>\u8FD8\u6CA1\u6709\u4E0A\u4F20\u8DDF\u7EC3\u52A8\u4F5C</p><p style="font-size:11px">\u62CD\u7167\u4E0A\u4F20\u4F60\u7684\u8BAD\u7EC3\u52A8\u4F5C\u5427</p></div>';
  return '<h3 style="font-size:14px;font-weight:600;margin-bottom:8px">\U0001f4cb \u5DF2\u4E0A\u4F20\u8DDF\u7EC3\u52A8\u4F5C</h3>'+cl.map(function(e,i){
    var img=e.photo?'<img src="'+e.photo+'" style="width:100%;border-radius:var(--radius) var(--radius) 0 0;max-height:200px;object-fit:cover" onclick="previewImg(\\x27'+e.photo+'\\x27)" loading="lazy">':'<div style="width:100%;height:140px;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;font-size:48px;border-radius:var(--radius) var(--radius) 0 0">\U0001f3cb\uFE0F</div>';
    return'<div class="custom-ex-card">'+img+'<div class="ex-body"><div style="display:flex;align-items:center;justify-content:space-between"><div class="ex-title">'+e.name+'</div><button class="btn btn-sm" style="background:rgba(255,59,48,.1);color:var(--danger);border:none;padding:4px 12px;border-radius:12px" onclick="rmCEx('+i+')">\u5220\u9664</button></div><div class="ex-desc">'+(e.desc||'')+'</div><div class="ex-date">'+fd(e.date)+' \u4E0A\u4F20</div></div></div>';
  }).join('');
}"""

new_custom_ex = """function renderCustomExList2(cl){
  if(!cl||cl.length===0)return'<div class="empty-state"><div class="empty-icon">\U0001f4f7</div><p>\u8FD8\u6CA1\u6709\u4E0A\u4F20\u8DDF\u7EC3\u52A8\u4F5C</p><p style="font-size:11px">\u62CD\u7167\u4E0A\u4F20\u4F60\u7684\u8BAD\u7EC3\u52A8\u4F5C\u5427</p></div>';
  return '<div class="grid-2">'+cl.map(function(e,i){
    var img=e.photo?'<img src="'+e.photo+'" style="width:100%;border-radius:var(--radius) var(--radius) 0 0;height:120px;object-fit:cover" onclick="previewImg(\\x27'+e.photo+'\\x27)" loading="lazy">':'<div style="width:100%;height:120px;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;font-size:36px;border-radius:var(--radius) var(--radius) 0 0">\U0001f3cb\uFE0F</div>';
    return'<div class="custom-ex-card" style="margin-bottom:0">'+img+'<div class="ex-body" style="padding:10px"><div class="ex-title" style="font-size:13px">'+e.name+'</div><div class="ex-desc" style="font-size:10px">'+(e.desc||'')+'</div><div style="display:flex;justify-content:space-between;align-items:center;margin-top:4px"><span class="ex-date" style="font-size:9px">'+fd(e.date)+'</span><button class="btn btn-sm" style="background:rgba(255,59,48,.1);color:var(--danger);border:none;padding:2px 8px;border-radius:10px;font-size:10px" onclick="rmCEx('+i+')">\u5220\u9664</button></div></div></div>';
  }).join('')+'</div>';
}"""

if old_custom_ex in html:
    html = html.replace(old_custom_ex, new_custom_ex)
    changes += 1
    print("Custom exercise list updated to 2-column")

# ===== 8. Thoughts module: 2-column card layout =====
old_thoughts_list = """function renderThoughtsList(st,filterCat){
  var el=document.getElementById('thoughtsList');if(!el)return;
  var notes=st.notes||[];
  if(filterCat&&filterCat!=='\u5168\u90E8')notes=notes.filter(function(n){return n.category===filterCat});
  if(notes.length===0){el.innerHTML='<div class="empty-state"><div class="empty-icon">\U0001f4a1</div><p>\u8FD8\u6CA1\u6709'+(filterCat&&filterCat!=='\u5168\u90E8'?filterCat+'\u5206\u7C7B\u7684':'')+'\u7B14\u8BB0</p><p style="font-size:11px">\u8BB0\u5F55\u4F60\u7684\u7075\u611F\u5427</p></div>';return}
  var allNotes=st.notes||[];
  el.innerHTML=notes.map(function(n,i){
    var originalIdx=allNotes.indexOf(n);
    var catTag='<span class="tag"'+(n.category==='\u7075\u611F'?' style="background:rgba(175,82,222,.1);color:#af52de"':n.category==='\u788E\u788E\u5FF5'?' style="background:rgba(255,45,85,.1);color:#ff2d55"':n.category==='\u5C0F\u65F6\u523B'?' style="background:rgba(52,199,89,.1);color:#34c759"':'')+'>'+(n.category||'\u5176\u4ED6')+'</span>';
    var imgHTML=n.photo?'<img src="'+n.photo+'" class="tc-img" onclick="previewImg(\\''+n.photo+'\\')" loading="lazy">':'';
    var aiLabel=n.ai?'<span style="font-size:9px;color:var(--accent);margin-left:4px">AI</span>':'';
    return'<div class="thought-card">'+imgHTML+'<button class="tc-delete" onclick="rmThought('+originalIdx+')">\u2715</button><div class="tc-body"><div class="tc-text">'+n.text+'</div><div class="tc-meta"><span>'+new Date(n.time).toLocaleString('zh-CN',{month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit'})+'</span><span style="display:flex;align-items:center;gap:4px">'+catTag+aiLabel+'</span></div></div></div>';
  }).join('');
}"""

# Replace with 2-column grid wrapper
new_thoughts_list = """function renderThoughtsList(st,filterCat){
  var el=document.getElementById('thoughtsList');if(!el)return;
  var notes=st.notes||[];
  if(filterCat&&filterCat!=='\u5168\u90E8')notes=notes.filter(function(n){return n.category===filterCat});
  if(notes.length===0){el.innerHTML='<div class="empty-state"><div class="empty-icon">\U0001f4a1</div><p>\u8FD8\u6CA1\u6709'+(filterCat&&filterCat!=='\u5168\u90E8'?filterCat+'\u5206\u7C7B\u7684':'')+'\u7B14\u8BB0</p><p style="font-size:11px">\u8BB0\u5F55\u4F60\u7684\u7075\u611F\u5427</p></div>';return}
  var allNotes=st.notes||[];
  el.innerHTML='<div class="grid-2">'+notes.map(function(n,i){
    var originalIdx=allNotes.indexOf(n);
    var catTag='<span class="tag"'+(n.category==='\u7075\u611F'?' style="background:rgba(175,82,222,.1);color:#af52de"':n.category==='\u788E\u788E\u5FF5'?' style="background:rgba(255,45,85,.1);color:#ff2d55"':n.category==='\u5C0F\u65F6\u523B'?' style="background:rgba(52,199,89,.1);color:#34c759"':'')+'>'+(n.category||'\u5176\u4ED6')+'</span>';
    var imgHTML=n.photo?'<img src="'+n.photo+'" class="tc-img" style="height:100px" onclick="previewImg(\\''+n.photo+'\\')" loading="lazy">':'';
    var aiLabel=n.ai?'<span style="font-size:9px;color:var(--accent);margin-left:4px">AI</span>':'';
    var cls=n.photo?'thought-card':'thought-card text-only';
    return'<div class="'+cls+'" style="margin-bottom:0">'+imgHTML+'<button class="tc-delete" onclick="rmThought('+originalIdx+')">\u2715</button><div class="tc-body" style="padding:10px"><div class="tc-text" style="font-size:13px">'+n.text+'</div><div class="tc-meta"><span style="font-size:9px">'+new Date(n.time).toLocaleString('zh-CN',{month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit'})+'</span><span style="display:flex;align-items:center;gap:4px">'+catTag+aiLabel+'</span></div></div></div>';
  }).join('')+'</div>';
}"""

if old_thoughts_list in html:
    html = html.replace(old_thoughts_list, new_thoughts_list)
    changes += 1
    print("Thoughts list updated to 2-column grid")

# ===== 9. Calorie: expand FOOD_DB =====
# Add more food items after the last food entry before ];
new_foods = """,
// v9 expanded: home dishes
{name:'西葫芦炒鸡蛋',cal:82,unit:'100g'},{name:'黄瓜凉面',cal:125,unit:'一份(约350g)'},{name:'蒜蓉空心菜',cal:32,unit:'100g'},
{name:'肉末茄子',cal:98,unit:'100g'},{name:'西红柿炖牛腩',cal:108,unit:'100g'},{name:'豆角焖面',cal:168,unit:'100g'},
{name:'青椒肉丝',cal:115,unit:'100g'},{name:'芹菜炒肉',cal:105,unit:'100g'},{name:'韭菜炒豆芽',cal:42,unit:'100g'},
{name:'蒜薹炒肉',cal:128,unit:'100g'},{name:'红烧茄子',cal:72,unit:'100g'},{name:'炒合菜',cal:65,unit:'100g'},
{name:'尖椒土豆丝',cal:82,unit:'100g'},{name:'家常炒饼',cal:175,unit:'100g'},{name:'蛋炒饼',cal:168,unit:'100g'},
{name:'炸酱面',cal:163,unit:'一碗(约450g)'},{name:'西红柿鸡蛋面',cal:110,unit:'一碗(约450g)'},
{name:'麻辣拌',cal:185,unit:'一份(约300g)'},{name:'烤冷面',cal:220,unit:'一份'},{name:'煎饼果子',cal:350,unit:'一个'},
{name:'肉夹馍',cal:228,unit:'一个'},{name:'凉拌黄瓜',cal:28,unit:'100g'},{name:'凉拌西红柿',cal:42,unit:'100g'},
{name:'拍黄瓜',cal:25,unit:'100g'},{name:'老虎菜',cal:38,unit:'100g'},{name:'皮蛋豆腐',cal:72,unit:'100g'},
{name:'凉拌木耳',cal:45,unit:'100g'},{name:'菠萝咕咾肉',cal:185,unit:'100g'},{name:'京酱肉丝',cal:178,unit:'100g'},
{name:'孜然羊肉',cal:182,unit:'100g'},{name:'干锅花菜',cal:85,unit:'100g'},{name:'干锅土豆片',cal:110,unit:'100g'},
{name:'干煸四季豆',cal:95,unit:'100g'},{name:'虎皮青椒',cal:45,unit:'100g'},{name:'可乐鸡翅',cal:178,unit:'100g'},
{name:'啤酒鸭',cal:168,unit:'100g'},{name:'剁椒鱼头',cal:82,unit:'100g'},{name:'毛血旺',cal:128,unit:'100g'},
{name:'回锅肉',cal:262,unit:'100g'},{name:'蚂蚁上树',cal:165,unit:'100g'},{name:'鱼香茄子',cal:82,unit:'100g'},
{name:'宫保虾球',cal:142,unit:'100g'},{name:'西湖醋鱼',cal:72,unit:'100g'},{name:'东坡肉',cal:325,unit:'100g'},
{name:'梅菜扣肉',cal:342,unit:'100g'},{name:'粉蒸肉',cal:268,unit:'100g'},{name:'红烧狮子头',cal:198,unit:'100g'},
{name:'糖醋排骨',cal:285,unit:'100g'},{name:'葱油鸡',cal:168,unit:'100g'},{name:'白切鸡',cal:145,unit:'100g'},
{name:'盐焗鸡',cal:172,unit:'100g'},{name:'清炒虾仁',cal:62,unit:'100g'},{name:'油焖大虾',cal:142,unit:'100g'},
{name:'葱姜炒蟹',cal:118,unit:'100g'},{name:'蛤蜊蒸蛋',cal:52,unit:'100g'},{name:'韭菜炒蛤蜊',cal:58,unit:'100g'},
{name:'排骨炖豆角',cal:132,unit:'100g'},{name:'海带排骨汤',cal:68,unit:'100g'},{name:'玉米排骨汤',cal:78,unit:'100g'},
{name:'山药排骨汤',cal:72,unit:'100g'},{name:'虫草花鸡汤',cal:65,unit:'100g'},{name:'乌鸡汤',cal:72,unit:'100g'},
// v9 expanded: snacks
{name:'薯片',cal:532,unit:'100g'},{name:'魔芋爽',cal:84,unit:'100g'},{name:'辣条',cal:435,unit:'100g'},
{name:'锅巴',cal:498,unit:'100g'},{name:'虾条',cal:510,unit:'100g'},{name:'旺旺仙贝',cal:485,unit:'100g'},
{name:'旺旺雪饼',cal:478,unit:'100g'},{name:'上好佳鲜虾片',cal:502,unit:'100g'},{name:'乐事薯片',cal:542,unit:'100g(约一包142g=770kcal)'},
{name:'奥利奥',cal:486,unit:'100g'},{name:'趣多多',cal:492,unit:'100g'},{name:'好丽友派',cal:425,unit:'100g'},
{name:'达利园蛋黄派',cal:418,unit:'100g'},{name:'沙琪玛',cal:506,unit:'100g'},{name:'桃酥',cal:483,unit:'100g'},
{name:'老婆饼',cal:385,unit:'100g'},{name:'蛋黄酥',cal:388,unit:'100g'},{name:'凤梨酥',cal:425,unit:'100g'},
{name:'牛轧糖',cal:435,unit:'100g'},{name:'大白兔奶糖',cal:408,unit:'100g'},{name:'德芙巧克力',cal:534,unit:'100g'},
{name:'费列罗',cal:582,unit:'100g'},{name:'士力架',cal:482,unit:'100g(一条51g=246kcal)'},
{name:'百奇饼干棒',cal:495,unit:'100g'},{name:'百力滋',cal:482,unit:'100g'},{name:'格力高',cal:490,unit:'100g'},
{name:'咪咪虾条',cal:525,unit:'100g'},{name:'亲亲虾条',cal:512,unit:'100g'},{name:'上好佳洋葱圈',cal:518,unit:'100g'},
{name:'瓜子(葵花籽)',cal:582,unit:'100g'},{name:'南瓜子',cal:574,unit:'100g'},{name:'西瓜子',cal:556,unit:'100g'},
{name:'夏威夷果',cal:718,unit:'100g'},{name:'碧根果',cal:691,unit:'100g'},{name:'巴旦木',cal:578,unit:'100g'},
{name:'葡萄干',cal:344,unit:'100g'},{name:'红枣',cal:276,unit:'100g'},{name:'枸杞',cal:349,unit:'100g'},
{name:'桂圆干',cal:319,unit:'100g'},{name:'芒果干',cal:348,unit:'100g'},{name:'香蕉片',cal:519,unit:'100g'},
{name:'山楂片',cal:372,unit:'100g'},{name:'果丹皮',cal:321,unit:'100g'},{name:'话梅',cal:168,unit:'100g'},
{name:'溜溜梅',cal:278,unit:'100g'},{name:'牛肉干',cal:318,unit:'100g'},{name:'猪肉脯',cal:378,unit:'100g'},
{name:'鱿鱼丝',cal:298,unit:'100g'},{name:'鱼片干',cal:285,unit:'100g'},{name:'泡椒凤爪',cal:156,unit:'100g'},
{name:'卤鸡爪',cal:215,unit:'100g'},{name:'卤鸭脖',cal:178,unit:'100g'},{name:'鸭锁骨',cal:168,unit:'100g'},
{name:'鸭舌',cal:202,unit:'100g'},{name:'周黑鸭鸭脖',cal:185,unit:'100g'},{name:'绝味鸭脖',cal:192,unit:'100g'},
// v9 expanded: beverages
{name:'雪碧',cal:49,unit:'100ml'},{name:'芬达',cal:48,unit:'100ml'},{name:'美年达',cal:48,unit:'100ml'},
{name:'红牛',cal:45,unit:'100ml'},{name:'脉动',cal:21,unit:'100ml'},{name:'尖叫',cal:24,unit:'100ml'},
{name:'宝矿力水特',cal:26,unit:'100ml'},{name:'农夫山泉维他命水',cal:18,unit:'100ml'},
{name:'元气森林',cal:0,unit:'100ml(0糖)'},{name:'零度可乐',cal:0,unit:'100ml'},{name:'东方树叶',cal:0,unit:'100ml'},
{name:'三得利乌龙茶',cal:0,unit:'100ml'},{name:'茶兀',cal:28,unit:'100ml'},{name:'阿萨姆奶茶',cal:58,unit:'100ml'},
{name:'营养快线',cal:52,unit:'100ml'},{name:'AD钙奶',cal:38,unit:'100ml'},{name:'养乐多',cal:68,unit:'100ml'},
{name:'优酸乳',cal:42,unit:'100ml'},{name:'真果粒',cal:45,unit:'100ml'},{name:'纯甄',cal:65,unit:'100ml'},
{name:'安慕希',cal:78,unit:'100ml'},{name:'莫斯利安',cal:75,unit:'100ml'},{name:'燕麦奶',cal:45,unit:'100ml'},
{name:'椰子水',cal:18,unit:'100ml'},{name:'王老吉',cal:32,unit:'100ml'},{name:'加多宝',cal:32,unit:'100ml'},
// v9 expanded: ice cream & desserts
{name:'可爱多',cal:178,unit:'一支(67g)'},{name:'梦龙',cal:232,unit:'一支(64g)'},{name:'巧乐兹',cal:195,unit:'一支(75g)'},
{name:'绿色心情',cal:82,unit:'一支(70g)'},{name:'老冰棍',cal:45,unit:'一支(70g)'},{name:'东北大板',cal:168,unit:'一支(75g)'},
{name:'八喜冰淇淋',cal:198,unit:'100g'},{name:'哈根达斯',cal:268,unit:'100g'},{name:'DQ暴风雪',cal:225,unit:'中杯'},
{name:'双皮奶',cal:112,unit:'一碗(约200g)'},{name:'杨枝甘露',cal:152,unit:'一碗(约300g)'},{name:'烧仙草',cal:145,unit:'一碗(约350g)'},
{name:'芋圆',cal:158,unit:'一碗(约250g)'},{name:'冰粉',cal:32,unit:'一碗(约300g)'},{name:'凉虾',cal:28,unit:'一碗(约300g)'},
{name:'龟苓膏',cal:55,unit:'一碗(约250g)'},{name:'布丁',cal:125,unit:'100g'},{name:'慕斯蛋糕',cal:325,unit:'100g'},
{name:'提拉米苏',cal:342,unit:'100g'},{name:'芝士蛋糕',cal:358,unit:'100g'},
// v9 expanded: street food
{name:'烤串(羊肉)',cal:218,unit:'一串(约50g)'},{name:'烤面筋',cal:142,unit:'一串'},{name:'烤鱿鱼',cal:95,unit:'一串(约80g)'},
{name:'烤鸡翅',cal:158,unit:'一串(两个)'},{name:'烤肠',cal:125,unit:'一根'},{name:'烤玉米',cal:168,unit:'一根'},
{name:'炸鸡排',cal:285,unit:'一块(约150g)'},{name:'炸鸡柳',cal:272,unit:'一份(约150g)'},{name:'炸薯条',cal:312,unit:'中份'},
{name:'炸年糕',cal:245,unit:'一份(约150g)'},{name:'鸡米花',cal:268,unit:'一份(约120g)'},{name:'上校鸡块',cal:252,unit:'一份(5块)'},
{name:'章鱼小丸子',cal:168,unit:'一份(6个)'},{name:'鸡蛋仔',cal:285,unit:'一份'},{name:'华夫饼',cal:291,unit:'100g'},
{name:'手抓饼',cal:345,unit:'一个'},{name:'杂粮煎饼',cal:285,unit:'一个'},{name:'烤红薯',cal:98,unit:'一个(约200g)'},
{name:'糖炒栗子',cal:212,unit:'100g'},{name:'爆米花',cal:387,unit:'100g'},{name:'棉花糖',cal:385,unit:'100g'},
// v9 expanded: convenience store foods
{name:'饭团(金枪鱼)',cal:185,unit:'一个'},{name:'三明治',cal:248,unit:'一个'},{name:'寿司拼盘',cal:325,unit:'一盒(约200g)'},
{name:'关东煮(综合)',cal:95,unit:'一份(约300g)'},{name:'茶叶蛋',cal:68,unit:'一个'},{name:'玉米热狗',cal:185,unit:'一根'},
{name:'包子(肉)',cal:128,unit:'一个(约80g)'},{name:'包子(菜)',cal:85,unit:'一个(约80g)'},{name:'豆沙包',cal:175,unit:'一个(约100g)'},
{name:'奶黄包',cal:168,unit:'一个(约60g)'},{name:'叉烧包',cal:152,unit:'一个(约70g)'},{name:'小笼包',cal:215,unit:'一笼(6个)'},
{name:'煎饺',cal:252,unit:'一份(6个)'},{name:'锅贴',cal:245,unit:'一份(6个)'},{name:'生煎包',cal:278,unit:'一份(4个)'},
// v9 expanded: mixed combos
{name:'黄焖鸡米饭',cal:520,unit:'一份(约400g米饭+菜)'},{name:'咖喱鸡肉饭',cal:485,unit:'一份(约400g)'},
{name:'卤肉饭',cal:620,unit:'一份(约400g)'},{name:'鸡腿饭',cal:550,unit:'一份'},{name:'排骨饭',cal:580,unit:'一份'},
{name:'麻辣香锅',cal:195,unit:'100g'},{name:'麻辣拌',cal:185,unit:'一份(约300g)'},{name:'麻辣烫(清汤)',cal:165,unit:'一份(约500g)'},
{name:'麻辣烫(骨汤)',cal:245,unit:'一份(约500g)'},{name:'冒菜',cal:220,unit:'一份(约500g)'},{name:'钵钵鸡',cal:178,unit:'100g'},
{name:'板面',cal:382,unit:'一碗(约500g)'},{name:'牛肉板面',cal:420,unit:'一碗(约500g)'},{name:'安徽板面',cal:395,unit:'一碗(约500g)'},
"""

# Find the last food entry before '];'
# The pattern is: {name:'食用油',cal:899,unit:'100g'}\n];
old_food_end = "{name:'\u98DF\u7528\u6CB9',cal:899,unit:'100g'}\n];"
if old_food_end in html:
    html = html.replace(old_food_end, "{name:'\u98DF\u7528\u6CB9',cal:899,unit:'100g'}," + new_foods + "\n];")
    changes += 1
    print("Food DB expanded")
else:
    # Try broader pattern
    print("WARNING: Food DB end pattern not found, trying alternative...")
    # Search for the last food entry
    idx = html.rfind("{name:'\u98DF\u7528\u6CB9'")
    if idx > 0:
        print(f"Found食用油 at {idx}")

# ===== 10. Fix rmCEx to use correct index =====
# The custom exercise deletion needs to work with the full custom array
old_rm = "function rmCEx(i){showConfirm('\u5220\u9664\u52A8\u4F5C'"
if old_rm in html:
    # Ensure it uses the full st.custom array, not the filtered one
    pass

# Save the result
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nTotal changes applied: {changes}")
print("index.html v9 saved.")
