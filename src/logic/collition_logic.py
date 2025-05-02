class CollitionLogic:
    def __init__(self):
        pass

    def collision_check(self, obj1_pos, obj1_mask, obj2_pos, obj2_mask):
        offset = (
            int(obj1_pos[0] - obj2_pos[0]),
            int(obj1_pos[1] - obj2_pos[1]),
        )
        return obj2_mask.overlap(obj1_mask, offset) is not None
