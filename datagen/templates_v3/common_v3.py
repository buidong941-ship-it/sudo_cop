"""Hàm dựng template dùng chung cho bộ v3 (không chứa câu thoại nào)."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
PN = "p.short + ((' size ' + str(p.size) + ' màu ' + p.color_vi) if p.size else '')"
NOTE = "Bộ v3 (D45), mô phỏng do nhóm viết, không phải bộ test của BTC. Mọi con số lấy từ eval/mock_tools.py theo ngày gọi."


def T(tid, split, persona, hard, choose, dates, calls, let=None, require=None, instances=None, no_sunday=None, note="", level="M2"):
    if instances is None:   # mặc định: holdout 4, dev 6; template cần khách CRM có định danh kênh: 3 (CRM có hạn)
        instances = 3 if "kind='crm'" in choose.get("cust", "") else (4 if split == "holdout" else 6)
    t = {"template_id": f"V3-{tid}-{split}", "split": split, "instances": instances, "choose": choose, "dates": dates,
         "let": let or {}, "require": require or [],
         "scenario": {"level": level, "persona": persona, "hard_case": hard, "notes": (note + " " + NOTE).strip(), "calls": calls}}
    if no_sunday:
        t["no_sunday"] = no_sunday
    return t


ONE = {"call_1": "d1"}
TWO = {"call_1": "d1", "call_2": "add(d1,gap)"}
THREE = {"call_1": "d1", "call_2": "add(d1,g1)", "call_3": "add(add(d1,g1),g2)"}
ADDR = {"address": "cust.address"}

