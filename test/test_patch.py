import pytest
from pyggi.base import Patch
from pyggi.line import LineProgram as Program
from pyggi.base.custom_operator import LineDeletion, LineMoving


@pytest.fixture(scope='session')
def setup():
    program = Program('./resource/Triangle_bug')
    assert len(program.target_files) == 1
    assert program.target_files[0] == 'Triangle.java'

    patch = Patch(program)
    return patch, program


class TestPatch(object):

    def test_init(self, setup):
        patch, program = setup

        assert patch.program == program
        assert patch.fitness == None
        assert patch.elapsed_time == None
        assert patch.compiled == True
        assert len(patch.edit_list) == 0

    def test_str(self, setup):
        patch, program = setup

        assert ' | '.join(list(map(str, patch.edit_list))) == str(patch)

    def test_len(self, setup):
        patch, program = setup

        assert len(patch.edit_list) == len(patch)

    def test_eq(self, setup):
        patch, program = setup
        program2 = Program('./resource/Triangle_bug')
        patch2 = Patch(program2)

        assert patch == patch2

    def test_clone(self, setup):
        patch, program = setup
        cloned_patch = patch.clone()

        assert cloned_patch.program == patch.program
        assert cloned_patch == patch
        assert cloned_patch.fitness == None

    def test_add(self, setup):
        patch, program = setup
        deletion_operator = LineDeletion
        deletion_instance = deletion_operator.create(program)
        patch.add(deletion_instance)

        assert len(patch) == 1
        assert patch.edit_list[0] == deletion_instance

        moving_operator = LineMoving
        moving_instance = moving_operator.create(program)
        patch.add(moving_instance)

        assert len(patch) == 2
        assert patch.edit_list[1] == moving_instance

    def test_get_atomics(self, setup):
        patch, program = setup
    
        assert len(patch.get_atomics('LineReplacement')) == 2
        assert len(patch.get_atomics('LineInsertion')) == 1
        
        atomics = patch.get_atomics()
        count = 0
        for edit in patch.edit_list:
            for atomic in edit.atomic_operators:
                assert atomic in atomics
                count += 1
        assert count == len(atomics)

    def test_apply(self, setup):
        patch, program = setup

        assert len(program.contents['Triangle.java']) + len(
            patch.get_atomics('LineInsertion'))== len(patch.apply()['Triangle.java'])

    def test_run_test(self, setup):
        patch, program = setup
        patch.run_test()
        
        assert len(patch) > 0
        assert patch.compiled in [True, False]
        assert patch.elapsed_time > 0

    def test_remove(self, setup):
        patch, program = setup
        old_patch = patch.clone()
        patch.remove(0)

        assert len(patch) == len(old_patch) - 1
        assert patch.edit_list == old_patch.edit_list[1:]
