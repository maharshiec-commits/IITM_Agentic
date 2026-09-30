from src.memory.store import MemoryStore, MemoryItem

def test_memory_store_user_roundtrip(tmp_path):
    ms = MemoryStore(str(tmp_path / "mem.db"))
    ms.upsert_user_memory("u1", MemoryItem(key="os", value="Windows", confidence=0.9))
    got = ms.get_user_memory("u1")
    assert got["os"] == "Windows"

def test_memory_store_case_roundtrip(tmp_path):
    ms = MemoryStore(str(tmp_path / "mem.db"))
    ms.upsert_case_memory("c1", "last_decision", "resolve_guidance")
    got = ms.get_case_memory("c1")
    assert got["last_decision"] == "resolve_guidance"
