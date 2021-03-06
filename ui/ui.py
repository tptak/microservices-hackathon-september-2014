import time

class UI(object):
    def __init__(self):
        import publisher
        import printer
        self.publisher = publisher.Publisher()
        self.printer = printer.BoardPrinter()
        self.run_printer_in_thread()
        self.new_game()

    def new_game(self):
        self.id = str(time.time())
        self.printer.set_id(self.id)
        self.game_start()

    def game_start(self):
        self.publish_action("go!!!!", topic='game.started',
                extra={'id': self.id}
                )

    def publish_action(self, action, topic='game', channel='ui', extra={}):
        data = {'action': action,
                'id': self.id,}
        data.update(extra)
        self.publisher.publish(topic, data)

    def run_printer_in_thread(self):
        import thread
        thread.start_new_thread(self.printer.run, ())

    def run(self):
        return self._run()
        import thread
        thread.start_new_thread(self._run, ())

    def _run(self):
        self.running = True
        while self.running:
            self.read_key()

    def quit(self):
        self.publish_action('quit')
        self.running = False

    def move_left(self):
        self.publish_action('left', topic='game.key')

    def move_right(self):
        self.publish_action('right', 'game.key')

    def publish_sample_board(self):
        self.publisher.publish('ui',
            {'board': [['x']*16]*30})

    def read_key(self):
        import term
        key = term.getch()
        if key == 'a':
            self.move_left()
        elif key == 'd':
            self.move_right()
        elif key == 'q' or key == '\x03':
            self.quit()
        elif key == 'n':
            self.new_game()
#         elif key == '0':
#             self.publish_sample_board()
        else:
            #print "bad key, use 'a', 'd' or 'q' to quit"
            pass




