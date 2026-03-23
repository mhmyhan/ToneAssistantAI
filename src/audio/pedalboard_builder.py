from pedalboard import Pedalboard, Compressor, Distortion, Chorus, Delay, Reverb, Limiter


def build_demo_board():
    # ompressor (Even out the input)
    comp = Compressor(threshold_db=-20, ratio=3)
    
    # Distortion
    dist = Distortion(drive_db=25)
    
    # Delay - Careful, possible re-instance may kill delay before it has a chance to play
    delay = Delay(delay_seconds=0.35, feedback=0.4, mix=0.3)
    
    # 4. Limiter
    # This prevents speakers from exploding when drive is high
    limiter = Limiter(threshold_db=-3.0, release_ms=100.0)

    # Assemble the board
    board = Pedalboard([comp, dist, delay, limiter])

    return board, {
        "compressor": comp,
        "distortion": dist,
        "delay": delay,
        "limiter": limiter
    }