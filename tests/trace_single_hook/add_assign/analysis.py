from dynapyt.analyses.BaseAnalysis import BaseAnalysis


class TestAnalysis(BaseAnalysis):
    def begin_execution(self):
        print("begin execution")

    def end_execution(self):
        print("end execution")

    def add_assign(self, dyn_ast, iid, left, right):
        print(f"add_assign: {left()} += {right}")
