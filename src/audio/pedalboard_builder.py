from pedalboard import Pedalboard, Compressor, Distortion, Chorus, Delay, Reverb


def build_demo_board():

    dist = Distortion(
        drive_db=25
    )

    delay = Delay(
        delay_seconds=0.35,
        feedback=0.4,
        mix=0.3
    )
    
    comp = Compressor(
        threshold_db=-20,
        ratio=3
    )
    
    chorus = Chorus(
        rate_hz=1.5,
        depth=0.4
    )
    
    reverb = Reverb(
        room_size=0.5
    )

    board = Pedalboard([comp, dist, chorus, delay, reverb])

    return board, {
        "compressor": comp,
        "distortion": dist,
        "chorus": chorus,
        "delay": delay,
        "reverb": reverb
    }
