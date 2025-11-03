class CurrentState:
    def __init__(
        self,
        init_frag_cnt,
        init_cert_cnt,
        char5_pool,
        char4_pool,
        rc5_pool,
        rc4_pool,
        rc3_pool,
        init_ticket_cnt=0,
        init_disk_cnt=0,
    ):
        self.frag_cnt = init_frag_cnt
        self.cert_cnt = init_cert_cnt
        self.char5_pool = char5_pool
        self.char4_pool = char4_pool
        self.rc5_pool = rc5_pool
        self.rc4_pool = rc4_pool
        self.rc3_pool = rc3_pool
        self.ticket_cnt = init_ticket_cnt
        self.disk_cnt = init_disk_cnt

    def __str__(self):
        return (
            f"frag_cnt: {self.frag_cnt}, ticket_cnt: {self.ticket_cnt}, disk_cnt: {self.disk_cnt}, cert_cnt: {self.cert_cnt}\n"
            + f"5★: {self.char5_pool}\n4★: {self.char4_pool}\n"
            + f"5★RC: {self.rc5_pool}\n4★RC: {self.rc4_pool}\n3★RC: {self.rc3_pool}"
        )


if __name__ == "__main__":
    pass
