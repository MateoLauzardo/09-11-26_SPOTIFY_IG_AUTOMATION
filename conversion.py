
#This just formats milliseconds its, minutes and seconds
def fmt_ms(ms):
    seconds = ms // 1000
    return f"{seconds // 60}:{seconds % 60:02d}"

