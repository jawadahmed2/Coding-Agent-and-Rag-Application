class WebhookHandler:
    def __init__(self, code_generator, code_tester, git_manager):
        self.code_generator = code_generator
        self.code_tester = code_tester
        self.git_manager = git_manager

    def handle_push_event(self, payload):
        branch = payload['ref'].split('/')[-1]

        if branch == 'main':
            try:
                generated_code = self.code_generator.generate_code("fibonacci")
                is_valid, test_output = self.code_tester.test_code(generated_code)

                if is_valid:
                    file_path = 'generated_code.py'
                    with open(file_path, 'w') as f:
                        f.write(generated_code)

                    self.git_manager.commit_and_push(file_path, "Add generated Fibonacci function")
                    return {'message': 'Code generated, tested, and pushed successfully'}, 200
                else:
                    return {'message': 'Generated code failed tests', 'test_output': test_output}, 400
            except Exception as e:
                return {'message': f'Error in code generation or testing: {str(e)}'}, 500

        return {'message': 'No action taken for this event'}, 200