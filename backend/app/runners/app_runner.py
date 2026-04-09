import json
from uuid import uuid4

from app.runners.base import BaseRunner
from app.schemas.common import RunRequest, RunResult, StepResult


class AppRunner(BaseRunner):
    engine_name = "app"

    def run(self, request: RunRequest) -> RunResult:
        device_id = str(request.params.get('device_id', 'emulator-5554'))
        app_package = str(request.params.get('app_package', 'com.demo.app'))
        app_activity = str(request.params.get('app_activity', 'com.demo.app.MainActivity'))
        script_path = str(request.params.get('script_path', 'scripts/demo.air'))
        expect = str(request.params.get('assert_keyword', 'success')).strip()
        env_name = str(request.params.get('env_name', '')).strip()
        steps = self._parse_steps(str(request.params.get('steps_json', '[]')))

        details: list[StepResult] = [
            StepResult(name='connect_device', status='passed', message=f'{device_id} online'),
            StepResult(name='start_session', status='passed', message=f'{app_package}/{app_activity}'),
            StepResult(name='load_script', status='passed', message=script_path),
        ]

        fake_screen = {
            'id=welcome': 'Welcome Demo',
            'id=status': 'success',
            'id=toast': 'Login Success',
        }
        passed = True
        elapsed_ms = 380

        for idx, step in enumerate(steps, start=1):
            action = str(step.get('action', '')).strip().lower()
            target = str(step.get('target', '')).strip()
            value = str(step.get('value', '')).strip()
            step_name = f'{idx:02d}_{action or "unknown"}'

            if action == 'wait':
                wait_ms = self._safe_int(step.get('ms', 500), default=500)
                elapsed_ms += wait_ms
                details.append(StepResult(name=step_name, status='passed', message=f'wait={wait_ms}ms'))
                continue

            if action in {'tap', 'input', 'swipe', 'launch_app'}:
                message = f'{action} target={target}' if target else action
                if value:
                    message = f'{message}, value={value}'
                details.append(StepResult(name=step_name, status='passed', message=message))
                elapsed_ms += 220
                if action == 'input' and target:
                    fake_screen[target] = value
                continue

            if action in {'assert_text', 'assert_exists'}:
                actual = fake_screen.get(target, '')
                is_ok = (value in actual) if action == 'assert_text' else bool(actual)
                details.append(
                    StepResult(
                        name=step_name,
                        status='passed' if is_ok else 'failed',
                        message=f'target={target}, expected={value}, actual={actual}',
                    )
                )
                elapsed_ms += 160
                if not is_ok:
                    passed = False
                continue

            details.append(StepResult(name=step_name, status='failed', message=f'unsupported action={action}'))
            passed = False

        keyword_ok = expect in json.dumps(fake_screen, ensure_ascii=False) if expect else True
        if not keyword_ok:
            passed = False
        details.append(
            StepResult(
                name='assert_keyword',
                status='passed' if keyword_ok else 'failed',
                message=f'keyword={expect or "<none>"}',
            )
        )

        return RunResult(
            run_id=str(uuid4()),
            engine='app',
            status='passed' if passed else 'failed',
            duration_ms=elapsed_ms,
            steps=details,
        )

    @staticmethod
    def _parse_steps(raw: str) -> list[dict[str, object]]:
        try:
            parsed = json.loads(raw or '[]')
        except json.JSONDecodeError:
            return []
        if not isinstance(parsed, list):
            return []
        return [item for item in parsed if isinstance(item, dict)]

    @staticmethod
    def _safe_int(value: object, default: int = 0) -> int:
        try:
            return max(0, int(str(value)))
        except (TypeError, ValueError):
            return default
