import math

class GestureDescriptor:
    TRAPEZOIDS = [
        [4, 8, 3, 7],
        [8, 12, 7, 11],
        [12, 16, 11, 15],
        [16, 20, 15, 19],
        [2, 6, 1, 5],
        [6, 10, 5, 9],
        [10, 14, 9, 13],
        [14, 18, 13, 17]
    ]

    @staticmethod
    def calculate_angle(a, b, c):
        '''
        Calculate angle at point b formed by points a-b-c.
        '''
        ba = (a.x - b.x, a.y - b.y)
        bc = (c.x - b.x, c.y - b.y)
        dot = ba[0] * bc[0] + ba[1] * bc[1]
        mag_ba = math.hypot(*ba)
        mag_bc = math.hypot(*bc)
        if mag_ba * mag_bc == 0:
            return 0.0
        return math.degrees(math.acos(dot / (mag_ba * mag_bc)))

    @classmethod
    def compute_descriptor(cls, landmarks, hand_label):
        '''
        Compute descriptor vector from landmarks and hand label.
        '''
        # First element is hand type: 0 for left, 1 for right
        hand_flag = 0 if hand_label == 'Left' else 1
        descriptor = [hand_flag]

        # 32 angles for 8 trapezoids of interest
        for quad in cls.TRAPEZOIDS:
            for i in range(4):
                prev_idx = quad[i - 1]
                curr_idx = quad[i]
                next_idx = quad[(i + 1) % 4]
                angle = cls.calculate_angle(
                    landmarks[prev_idx], landmarks[curr_idx], landmarks[next_idx]
                )
                descriptor.append(angle)
        return descriptor
