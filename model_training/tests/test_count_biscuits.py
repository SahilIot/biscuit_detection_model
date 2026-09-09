from counting.count_biscuit import BiscuitCounter
def test_one_biscuit_is_counted_once():
    counter = BiscuitCounter()
    # Frame 1: biscuit appears.
    counter.update([{"track_id": 1,"center": (100, 100),}])
    assert counter.total_biscuits == 1
    # Frame 2: same biscuit moves.
    counter.update([{"track_id": 1, "center": (110, 100),}])
    assert counter.total_biscuits == 1
    # Frame 3: same biscuit moves again.
    counter.update([{"track_id": 1,"center": (120, 100),}])
    assert counter.total_biscuits == 1

def test_two_biscuits_are_counted():
    counter = BiscuitCounter()
    # Biscuit 1
    counter.update([{"track_id": 1,"center": (100, 100),}])
    # Biscuit 2
    counter.update([{"track_id": 2,"center": (300, 100),}])
    assert counter.total_biscuits == 2

def test_same_biscuit_with_new_tracker_id_is_not_counted_again():
    counter = BiscuitCounter( max_match_distance=80)
    # Original tracker ID.
    counter.update([{"track_id": 1,"center": (100, 100),}])
    assert counter.total_biscuits == 1
    # ByteTrack loses the old ID and assigns a new one.
    # The position is still very close.
    counter.update([{"track_id": 99,"center": (110, 105),}])
    # Must still be the same biscuit.
    assert counter.total_biscuits == 1

def test_new_biscuit_after_existing_biscuit():
    counter = BiscuitCounter()
    # Biscuit 1.
    counter.update([{"track_id": 1,"center": (100, 100),}])
    assert counter.total_biscuits == 1
    # Same biscuit.
    counter.update([{"track_id": 1,"center": (120, 100),}])
    assert counter.total_biscuits == 1
    # New biscuit far away.
    counter.update([{"track_id": 2,"center": (500, 100),}])
    assert counter.total_biscuits == 2

def test_multiple_biscuits_in_same_frame():
    counter = BiscuitCounter()
    counter.update([
        {"track_id": 1,"center": (100, 100),},
        {"track_id": 2,"center": (300, 100),},
        {"track_id": 3,"center": (500, 100),},])
    assert counter.total_biscuits == 3

def test_same_biscuit_across_many_frames():

    counter = BiscuitCounter()
    for frame in range(20):
        counter.update([{"track_id": 1,"center": (100 + frame * 5,100,),}])
    assert counter.total_biscuits == 1

def test_temporarily_missing_biscuit():

    counter = BiscuitCounter( max_missed_frames=5)
    # Biscuit appears.
    counter.update([{"track_id": 1,"center": (100, 100),}])
    assert counter.total_biscuits == 1
    # Biscuit disappears for 3 frames
    counter.update([])
    counter.update([])
    counter.update([])
    # Biscuit returns with a different tracker ID.
    counter.update([{"track_id": 50,"center": (110, 105),}])
    # It must still be Biscuit 1.
    assert counter.total_biscuits == 1

def test_far_away_new_biscuit_is_counted():
    counter = BiscuitCounter( max_match_distance=80)
    # Biscuit 1.
    counter.update([{"track_id": 1,"center": (100, 100),}])
    assert counter.total_biscuits == 1
    # Far-away detection = new biscuit.
    counter.update([{"track_id": 2,"center": (500, 500),}])
    assert counter.total_biscuits == 2