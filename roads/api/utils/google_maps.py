# utils/google_maps.py
from typing import Iterable, List, Tuple, Dict
import requests

def chunked(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i+n]

def fetch_distance_matrix_pairwise(
    pairs: Iterable[Tuple[Tuple[float, float], Tuple[float, float]]],
    api_key: str,
    session: requests.Session,
    batch_size: int = 25,
) -> List[Dict]:
    """
    Given [(orig_lat,orig_lng), (dest_lat,dest_lng)] pairs, fetch distance & duration per pair.
    Returns list aligned with input order:
      [{'origin_address','destination_address','distance_km','duration_min'}]
    Assumes pairs are aligned (i.e., we read the diagonal element per row).
    """
    results: List[Dict] = []
    pairs = list(pairs)

    for chunk in chunked(pairs, batch_size):
        origins = "|".join([f"{o[0]:.8f},{o[1]:.8f}" for (o, _) in chunk])
        dests   = "|".join([f"{d[0]:.8f},{d[1]:.8f}" for (_, d) in chunk])
        url = (
            "https://maps.googleapis.com/maps/api/distancematrix/json"
            f"?origins={origins}&destinations={dests}&key={api_key}"
        )

        try:
            data = session.get(url).json()
        except Exception:
            for _ in chunk:
                results.append({
                    "origin_address": "",
                    "destination_address": "",
                    "distance_km": 0.0,
                    "duration_min": 0.0,
                })
            continue

        origin_addrs = data.get("origin_addresses") or [""] * len(chunk)
        dest_addrs   = data.get("destination_addresses") or [""] * len(chunk)
        rows         = data.get("rows") or []

        for i in range(len(chunk)):
            try:
                el = rows[i]["elements"][i]  # diagonal mapping
                dist_km = round((el.get("distance", {}).get("value", 0) or 0) / 1000, 1)
                dur_min = round((el.get("duration", {}).get("value", 0) or 0) / 60, 1)
            except Exception:
                dist_km, dur_min = 0.0, 0.0

            results.append({
                "origin_address": origin_addrs[i] if i < len(origin_addrs) else "",
                "destination_address": dest_addrs[i] if i < len(dest_addrs) else "",
                "distance_km": dist_km,
                "duration_min": dur_min,
            })

    return results
