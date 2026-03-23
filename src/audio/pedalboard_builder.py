from pedalboard import Pedalboard, Compressor, Distortion, Delay, Limiter, Gain

def build_demo_board():
    comp = Compressor(threshold_db=-24, ratio=4)

    pre_gain = Gain(gain_db=10)   # boost into distortion
    dist = Distortion(drive_db=20)
    post_gain = Gain(gain_db=-8)  # reduce output after distortion

    delay = Delay(delay_seconds=0.35, feedback=0.4, mix=0.3)

    limiter = Limiter(threshold_db=-3.0, release_ms=100.0)

    board = Pedalboard([
        comp,
        pre_gain,
        dist,
        post_gain,
        delay,
        limiter
    ])

    return board, {
        "compressor": comp,
        "pre_gain": pre_gain,
        "distortion": dist,
        "post_gain": post_gain,
        "delay": delay,
        "limiter": limiter
    }
