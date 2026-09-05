def transition(state, event):
    allowed={('pending','pay'):'paid', ('pending','cancel'):'cancelled', ('paid','ship'):'shipped'}
    if (state,event) not in allowed: raise ValueError('invalid transition')
    return allowed[(state,event)]
