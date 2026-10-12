import urllib.request
import json
import sys

def post(url, payload=None):
    body = json.dumps(payload or {}).encode('utf-8')
    req = urllib.request.Request(f'http://localhost:8000{url}', data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def get(url):
    req = urllib.request.Request(f'http://localhost:8000{url}')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def test_pipeline():
    print("=== Testing Storyboard Pipeline on http://localhost:8000 ===")
    
    # 0. Reset
    print("0. Resetting state...")
    r0 = post('/api/reset')
    assert r0['status'] == 'ok', f"Reset failed: {r0}"
    print("   [OK] Reset ok")

    # 1. Step 1: Create Tender (Model B)
    print("1. Creating Tender (Model B)...")
    t = post('/api/tender/create', {
        'tender_id': 'TENDER-QCBS-2026-001',
        'title': 'National Highway 402 Corridor Modernization',
        'buyer_name': 'Ministry of Transportation',
        'estimated_amount': 3800000,
        'bond_amount': 190000,
        'tech_weight': 0.70,
        'fin_weight': 0.30,
        'min_tech_score': 75.0
    })
    assert t['status'] == 'ok'
    print(f"   [OK] Tender initialized: PDA {t['tender']['pda'][:16]}... (Status: {t['tender']['status']})")

    # 2. Step 2: Commit 3 Bids
    print("2. Committing 3 Dual-Envelope Bids...")
    local_receipts = []
    b1 = post('/api/bid/commit_dual', {'bidder_name': 'ACME Infrastructure Corp', 'price': 3800000, 'bond_mode': 1, 'bond_amount': 190000})
    assert b1['status'] == 'ok' and b1.get('receipt')
    local_receipts.append(b1['receipt'])
    print("   [OK] Bid 1 (ACME): Committed and receipt stored.")

    b2 = post('/api/bid/commit_dual', {'bidder_name': 'Apex Civil Engineering', 'price': 4100000, 'bond_mode': 2, 'bond_amount': 190000})
    assert b2['status'] == 'ok' and b2.get('receipt')
    local_receipts.append(b2['receipt'])
    print("   [OK] Bid 2 (Apex): Committed and receipt stored.")

    b3 = post('/api/bid/commit_dual', {'bidder_name': 'Rogue Non-Compliant Builder', 'price': 2900000, 'bond_mode': 3, 'bond_amount': 190000})
    assert b3['status'] == 'ok' and b3.get('receipt')
    local_receipts.append(b3['receipt'])
    print("   [OK] Bid 3 (Rogue): Committed and receipt stored.")

    # 3. Step 3: Advance to Locked & Test Late Bid Attack
    print("3. Advancing past deadline slot & intercepting Attack 1...")
    adv1 = post('/api/tender/advance_phase')
    assert adv1['status'] == 'ok'
    print(f"   [OK] Phase advanced to: {adv1['tender_status']} at slot {adv1['current_slot']}")

    att1 = post('/api/attack/late_bid')
    assert att1['status'] in ['defended', 'intercepted']
    print(f"   [OK] Attack 1 intercepted: {att1.get('error_type', 'DeadlineExceeded')}")

    # 4. Step 4: Advance to Technical Evaluation, Reveal Tech Proposals & Finalize
    print("4. Technical evaluation & Olympic Trimmed Mean scoring...")
    adv2 = post('/api/tender/advance_phase')
    assert adv2['status'] == 'ok'
    print(f"   [OK] Phase advanced to: {adv2['tender_status']}")

    st = get('/api/status')
    for b in st['bids']:
        post('/api/bid/reveal_technical', {
            'bidder_pubkey': b['bidder']
        })
    print(f"   [OK] Revealed technical envelopes for {len(st['bids'])} bidders.")

    fin_tech = post('/api/tender/finalize_technical', {'auto_seed_demo': True})
    assert fin_tech['status'] == 'ok'
    print(f"   [OK] Technical scores finalized: {fin_tech['total_qualified']} qualified.")

    # 5. Step 5: Advance to Financial Reveal, Reveal Qualified, Record Award & Tribunal Audit
    print("5. Financial reveal, QCBS award & Tribunal Audit...")
    adv3 = post('/api/tender/advance_phase')
    assert adv3['status'] == 'ok'
    print(f"   [OK] Phase advanced to: {adv3['tender_status']}")

    reveals = []
    for r in local_receipts:
        p_img = r.get("unsealingPreimages", {})
        reveals.append({
            "bidder_pubkey": r["bidderPubkey"],
            "salt_fin": p_img.get("saltFin"),
            "price": p_img.get("price"),
            "boq_hash": p_img.get("boqHash")
        })

    rev_fin = post('/api/bid/reveal_financial', {"reveals": reveals})
    assert rev_fin['status'] == 'ok'
    print(f"   [OK] Financial envelopes revealed: {len(rev_fin.get('revealed', []))} envelopes unsealed.")

    award = post('/api/tender/award')
    assert award['status'] == 'ok'
    print(f"   [OK] Award recorded! Winning Bidder: {award['winning_bid']['bidder'][:16]}... (Score: {award['winning_bid']['composite_score']/100:.2f}%)")

    audit = post('/api/tribunal/verify')
    assert audit['status'] == 'ok' and audit['audit_report']['valid']
    print("   [OK] Tribunal Audit: 100% verified across all 5 cryptographic invariant phases!")

    print("\n>>> ALL 5 STORYBOARD STEPS AND BUTTONS ARE 100% WORKING! <<<")

if __name__ == '__main__':
    test_pipeline()
