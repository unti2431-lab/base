import json, sys
sb = json.load(open(sys.argv[1]))
S = {s['shot_id']: s for s in sb['shots']}
order = [s['shot_id'] for s in sb['shots']]
def fr(sid):
    s = S[sid]; return [s['timeline_frame_start'], s['timeline_frame_end'], s['timeline_frame_end']-s['timeline_frame_start']+1]

# boundary decisions: (a, b, primary, secondary, motif)
B = [
("S001","S002","T1","T4,T6","M2"),("S002","S003","T2_tail","T6",""),("S004","S005","T2_head","T5","M3"),
("S005","S006","T2_tail","T1","M3"),("S006","S007","T3","T5","M2,M3"),("S008","S009","T1","T2_tail","window"),
("S014","S015","T2_head","T5,T7","M1"),("S015","S016","T2_tail","T6","M1"),("S018","S019","T2_head","T5","M3"),
("S019","S020","T2_tail","T7",""),("S020","S021","T2_head","",""),("S021","S022","T1","T2_tail","sign"),
("S037","S038","T1","T2_head","M4"),("S038","S039","T2_tail","T1","M4"),("S046","S047","T2_head","T6",""),
("S048","S049","T1","T2_tail","duct"),("S053","S054","T1","T2_head,T5","M4"),("S054","S055","T2_tail","T1","M4"),
("S057","S058","T2_head","",""),("S058","S059","T1","T2_tail","M4,duct"),("S061","S062","T2_head","T6",""),
("S062","S063","T2_tail","T7",""),("S065","S066","T1","T2_head","M2"),("S066","S067","T2_tail","T1","M2"),
("S067","S068","T2_head","",""),("S068","S069","T5","T2_tail","M1"),("S070","S071","T2_head","T6",""),
("S073","S074","T1","T2_tail","layers"),("S076","S077","T2_head","T7",""),("S077","S078","T1","T2_tail","layers"),
("S078","S079","T2_head","",""),("S080","S081","T1","T2_tail","M4"),("S086","S087","T1","T2_head","M4"),
("S087","S088","T2_tail","T6",""),("S090","S091","T2_head","T6","M4"),("S092","S093","M5_sync","T6","M5"),
("S098","S099","T2_head","",""),("S100","S101","T2_tail","",""),("S102","S103","T5","T2_head","M1"),
("S103","S104","T2_tail","T5","M1"),("S109","S110","T2_head","T7",""),("S111","S112","T5","T2_tail","M1"),
]
# sanity: these must equal the real type-change boundaries
real = [(a,b) for a,b in zip(order, order[1:]) if S[a]['shot_type'] != S[b]['shot_type']]
assert [(a,b) for a,b,*_ in B] == real, "boundary list mismatch"

# flow slot plans: sid -> (generation mode, notes)
F = {
"S002":("T1_KEYFRAME+MOTIONREF","center vanishing point = S001; forward dolly continuing S001 push-in"),
"S005":("T1_KEYFRAME","ceiling line height = S004 grey layer top"),
"S007":("BRIDGE","first frame = photoreal of S006 last frame (same pillars); 8s gen, use 32f; T5 grey band overlay"),
"S008":("T1_KEYFRAME","keep above-ground room + open window; window placed at S009 opening coords; fix cue text"),
"S015":("T1_KEYFRAME","floor guide line = M1 legend; cyan line T5 overlay"),
"S019":("T1_KEYFRAME","stair center axis aligned with S018 smoke line"),
"S021":("REGEN_FROM_2D_CARD","ceiling exit pictogram (no text) at S022 white block coords"),
"S038":("T1_KEYFRAME","fire door frame at S037/S039 wall x-position; M4 legend"),
"S047":("DEDUP_MACRO","exhaust grille macro; fix cue to match narration; extend into S048"),
"S048":("DEDUP_WIDE_EXTEND","wide of same ceiling via extend; duct at S049 upper-right box"),
"S054":("T1_KEYFRAME","door at S053/S055 door position; cyan air T5"),
"S058":("DEDUP_BRIDGE","photoreal of S059 unified section; 3-beat T5 overlays"),
"S062":("DEDUP_REALIZE","empty platform deep axis from Blender clay; distant rumble"),
"S066":("REGEN_FROM_2D_CARD","long platform axis + tunnel portals; perspective = S065 end"),
"S068":("T1_KEYFRAME","floor guide line emphasized (M1)"),
"S071":("REALIZE","train arrival/stop timing from Blender clay; unbranded"),
"S072":("PLAIN","car interior depth; no twin"),
"S073":("T1_KEYFRAME","seat slats at S074 slab heights/spacing"),
"S077":("T1_KEYFRAME","-1 stop grade; panel grain aligned to S078 layers"),
"S079":("T1_KEYFRAME","platform + stopped train side"),
"S080":("T1_KEYFRAME","closed door center at S081 white box coords"),
"S087":("T1_KEYFRAME","open door (no people) at S086 train door coords"),
"S091":("REALIZE_SHARED","one Blender clay gen: open-hold-close; S091 = open part"),
"S092":("REALIZE_SHARED+FIX","same gen close part; lights dim one step synced to S093"),
"S099":("REGEN_FROM_2D_CARD","generic emergency door release detail, no text"),
"S100":("BRIDGE_EXTEND","first frame = S099 last frame; pull back to wide of same device; currently HOLD"),
"S103":("REGEN_FROM_2D_CARD","unbranded fare gates; cyan line passes through"),
"S110":("GLOW_SHARED","lights off, photoluminescent marking macro"),
"S111":("GLOW_SHARED","same gen pull-back: device + usage marking relation"),
}
assert set(F) == {s for s in order if S[s]['shot_type']=='FLOW'}

twins = {}
for a,b,p,sec,m in B:
    for code in [p]+[x for x in sec.split(',') if x]:
        if code == "T2_tail":
            flow = a if S[a]['shot_type']=='FLOW' else None
            assert flow, (a,b)
            twins.setdefault(flow, set()).add("tail")
        if code == "T2_head":
            flow = b if S[b]['shot_type']=='FLOW' else None
            assert flow, (a,b)
            twins.setdefault(flow, set()).add("head")

jobs=[]
for sid,(mode,note) in F.items():
    s=S[sid]; f=fr(sid)
    jobs.append({"job_id":f"GEN-{sid}","type":"FLOW_SLOT_GENERATION","shot_id":sid,"mode":mode,
        "timeline_frames":{"start":f[0],"end":f[1],"count_30fps":f[2]},
        "generate_seconds":8,"min_v2v_source_ok":True,"candidates":3,
        "narration_status":s['narration_status'],"visual_cue_original":s['visual_cue'],"note":note})
    if sid in twins:
        jobs.append({"job_id":f"DG-{sid}","type":"OMNI_V2V_DIAGRAM_TWIN","shot_id":sid,
            "source":f"GEN-{sid} selected 8s master (24fps)","crossfade_at":sorted(twins[sid]),
            "crossfade_frames_30fps":"10-18","prompt_template":"J-DIAGRAM","gate":["G1","G2","G3"]})
extra=[("REALIZE-S062","S062"),("REALIZE-S071","S071"),("REALIZE-S091S092","S091,S092"),("REALIZE-S100","S100")]
for j,sid in extra: jobs.append({"job_id":j,"type":"OMNI_V2V_REALIZE","shots":sid.split(','),"input":"Blender B4 clay render >=3.2s with handles","prompt_template":"J-REALIZE"})
for sid in ["S007","S058","S100"]: jobs.append({"job_id":f"BRIDGE-{sid}","type":"OMNI_FIRST_LAST_FRAME","shot_id":sid,"prompt_template":"J-BRIDGE"})
jobs.append({"job_id":"MOTIONREF-S002","type":"OMNI_VIDEO_REFERENCE","shot_id":"S002","reference":"S001 camera move 3s clay","prompt_template":"J-MOTIONREF"})
jobs.append({"job_id":"FIX-S092","type":"OMNI_V2V_PARTIAL_EDIT","shot_id":"S092","edits":["doors fully closed","ceiling lights dim one step synced to S093 brightness step"],"prompt_template":"J-FIX"})
jobs.append({"job_id":"GLOW-S110S111","type":"OMNI_V2V_PARTIAL_EDIT","shots":["S110","S111"],"prompt_template":"J-GLOW"})

out={"schema":"LONG2_DIRECTION_OMNI_JOBS_V1","plan_doc":"DIRECTION_PLAN_v1.md",
 "status":"PROPOSAL_ONLY_NOT_PRODUCTION_APPROVAL","source_storyboard_created_kst":sb['created_kst'],
 "timeline":sb['timeline'],
 "rules":["Blender base pixels never pass through a generative model","Fact pixels (times, 160 m, 192, labels) only from Blender originals",
   "Original and diagram twin share identical trims and identical 24->30fps conversion","No people/faces/flames/text/numbers/logos/station names in Omni output",
   "Do not crop or inpaint visible watermarks; regenerate under a no-visible-mark export condition"],
 "lock_block":"LOCK: keep exact framing, camera path, timing and all geometry. NO people, NO faces, NO flames, NO fire, NO text, NO letters, NO numbers, NO logos, NO brand livery, NO station names, NO signage words. Present-day, unbranded, location-unspecified Korean-style metro interior.",
 "boundaries":[{"n":i+1,"from":a,"from_type":S[a]['shot_type'],"to":b,"to_type":S[b]['shot_type'],"cut_frame":S[b]['timeline_frame_start'],
   "primary":p,"secondary":[x for x in sec.split(',') if x],"motif":[x for x in m.split(',') if x]} for i,(a,b,p,sec,m) in enumerate(B)],
 "pilots":[{"id":"P1","shots":["S014","S015","S016"]},{"id":"P2","shots":["S090","S091","S092","S093"]},{"id":"P3","shots":["S005","S006","S007"]}],
 "jobs":jobs,
 "counts":{"boundaries":len(B),"flow_slots":len(F),"diagram_twins":len(twins),"jobs":len(jobs)}}
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
print(out['counts'], sorted(twins))
