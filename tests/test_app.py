import sys
from unittest.mock import patch

from demeuk import main
from pytest import raises


def calculate_line_numbers(file_name):
    lines = 0
    with open(file_name, 'rb') as file:
        for lines, line in enumerate(file):
            pass
    return lines + 1


def test_demeuk():
    testargs = ['demeuk', '-i', 'testdata/input1', '-o', 'testdata/output1', '-l', 'testdata/log1']
    with patch.object(sys, 'argv', testargs):
        main()

    line_num_input1 = calculate_line_numbers('testdata/input1')
    line_num_output1 = calculate_line_numbers('testdata/output1')
    line_num_log1 = calculate_line_numbers('testdata/log1')

    assert line_num_log1 == 4
    assert line_num_output1 == 9
    assert line_num_input1 == (line_num_output1 + line_num_log1)
    with open('testdata/output1') as file:
        filecontent = file.read()
        assert 'Password123!@"\n' in filecontent
        assert 'ǓǝǪǼȧɠ\n' in filecontent
        assert 'ʄʛʨʾϑϡϣЄ\n' in filecontent
        assert 'ϽϾϿЀЁЂЃЄЅІЇЈ\n' in filecontent
        assert '做戏之说\n' in filecontent
        assert 'Hyggelig123åmøtedeg!\n' in filecontent
        assert 'бонусов$123\n' in filecontent
        assert '!!!ееместной%%@!\n' in filecontent


def test_multithread():
    testargs = ['demeuk', '-i', 'testdata/input2', '-o', 'testdata/output2', '-j', '3']
    with patch.object(sys, 'argv', testargs):
        main()

    line_num_input1 = calculate_line_numbers('testdata/input2')
    line_num_output1 = calculate_line_numbers('testdata/output2')

    assert line_num_output1 == 8
    assert line_num_input1 == line_num_output1


def test_newline():
    testargs = ['demeuk', '-i', 'testdata/input3', '-o', 'testdata/output3']
    with patch.object(sys, 'argv', testargs):
        main()

    line_num_input1 = calculate_line_numbers('testdata/input3')
    line_num_output1 = calculate_line_numbers('testdata/output3')

    assert line_num_output1 == 8
    assert line_num_input1 == line_num_output1
    with open('testdata/output3') as file:
        filecontent = file.read()
        for x in range(7):
            assert f'line{x}\n' in filecontent


def test_tabchar():
    testargs = ['demeuk', '-i', 'testdata/input4', '-o', 'testdata/output4']
    with patch.object(sys, 'argv', testargs):
        main()

    line_num_output1 = calculate_line_numbers('testdata/output4')
    assert line_num_output1 == 2
    with open('testdata/output4') as file:
        filecontent = file.read()
        assert 'line:entry\n' in filecontent
        assert 'line2:entry2\n' in filecontent


def test_split_email():
    testargs = ['demeuk', '-i', 'testdata/input5', '-o', 'testdata/output5', '--remove-email', '-c']
    with patch.object(sys, 'argv', testargs):
        main()
    line_num_output = calculate_line_numbers('testdata/output5')
    assert line_num_output == 6
    with open('testdata/output5') as file:
        filecontent = file.read()
        assert 'line1\n' in filecontent
        assert 'email@example.com' not in filecontent
        assert 'alcatel-sbell' not in filecontent
        assert '\nline4\n' in filecontent
        assert '\nline5\n' in filecontent
        assert '\nline6\n' in filecontent


def test_googlengram():
    testargs = ['demeuk', '-i', 'testdata/input6', '-o', 'testdata/output6', '-g']
    with patch.object(sys, 'argv', testargs):
        main()
    line_num_output = calculate_line_numbers('testdata/output6')
    assert line_num_output == 4
    with open('testdata/output6') as f:
        filecontent = f.read()
        assert 'I\'ain\n' in filecontent
        assert 'I\'Afrique occidental\n' in filecontent
        assert 'I\'Allemagne\n' in filecontent
        assert 'I\'ain a\n' in filecontent


def test_coupe():
    testargs = ['demeuk', '-i', 'testdata/input7', '-o', 'testdata/output7', '-l', 'testdata/log7']
    with patch.object(sys, 'argv', testargs):
        main()

    line_num_output = calculate_line_numbers('testdata/output7')
    assert line_num_output == 2
    with open('testdata/output7') as f:
        filecontent = f.read()
        assert 'coupÉ' in filecontent
        assert 'LANCIA AURELIA B20 COUPÉ GT\n' in filecontent


def test_split():
    testargs = ['demeuk', '-i', 'testdata/input8', '-o', 'testdata/output8', '-c']
    with patch.object(sys, 'argv', testargs):
        main()

    line_num_output = calculate_line_numbers('testdata/output8')
    assert line_num_output == 4
    with open('testdata/output8') as f:
        filecontent = f.read()
        assert 'example.com' not in filecontent
        assert 'sub.example.com' not in filecontent
        assert 'example.guru' not in filecontent
        assert 'sub.test-example.com' not in filecontent


def test_output_encoding():
    testargs = ['demeuk', '-i', 'testdata/input1', '-o', 'testdata/output1', '--output-encoding', 'C']
    with patch.object(sys, 'argv', testargs):
        with raises(UnicodeEncodeError):
            main()


def test_input_encoding():
    testargs = ['demeuk', '-i', 'testdata/input9', '-o', 'testdata/output9', '--input-encoding', 'windows-1251,UTF-16']
    with patch.object(sys, 'argv', testargs):
        main()
    line_num_output = calculate_line_numbers('testdata/output9')
    assert line_num_output == 2
    with open('testdata/output9') as f:
        filecontent = f.read()
        assert '16THEBEST!!!\n' in filecontent
        assert '!!!ееместной%%@!\n' in filecontent


def test_delimiter():
    testargs = [
        'demeuk', '-i', 'testdata/input10', '-o', 'testdata/output10',
        '-l', 'testdata/log10',
        '--cut', '--delimiter', '/', '--cut-before', '--check-min-length', '1',
        '--check-max-length', '10',
        '--check-case',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    line_num_output = calculate_line_numbers('testdata/output10')
    assert line_num_output == 1
    with open('testdata/output10') as f:
        filecontent = f.read()
        assert 'cĳfer\n' in filecontent
        assert '3M\n' not in filecontent
        assert 'VERYVERYVERYVERYVERYVERYLONGLINE?\n' not in filecontent


def test_language_processing():
    testargs = [
        'demeuk', '-i', 'testdata/input11', '-o', 'testdata/output11',
        '-l', 'testdata/log11',
        '--cut', '--delimiter', '/', '--cut-before', '--check-min-length', '2',
        '--remove-punctuation', '--add-lower', '--add-latin-ligatures',
        '--add-split',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    line_num_output = calculate_line_numbers('testdata/output11')
    assert line_num_output == 29
    with open('testdata/output11') as f:
        filecontent = f.read()
        assert 'cĳfer\n' in filecontent
        assert 'cijfer\n' in filecontent
        assert '3M\n' in filecontent
        assert '3m\n' in filecontent
        assert '\ntest\n' in filecontent
        assert '3M-test\n' in filecontent
        assert 'St. Maarten\n' in filecontent
        assert 'St\n' in filecontent
        assert '\nMaarten\n' in filecontent
        assert 'Aai-Aai\n' in filecontent
        assert '3-hoekig\n' in filecontent
        assert '\nhoekig\n' in filecontent
        assert '3\n' not in filecontent
        assert 'Philipsburg.\n' not in filecontent
        assert 'Philipsburg\n' in filecontent


def test_fries():
    testargs = ['demeuk', '-i', 'testdata/input12', '-o', 'testdata/output12', '-l', 'testdata/log12', '--no-mojibake']
    with patch.object(sys, 'argv', testargs):
        main()
    with open('testdata/log12') as f:
        filecontent = f.read()
        assert 'West-Frysl' in filecontent
    with open('testdata/output12') as f:
        filecontent = f.read()
        assert 'West-Frysl‰n' not in filecontent


def test_cut_fields():
    testargs = [
        'demeuk', '-i', 'testdata/input13', '-o', 'testdata/output13', '-l', 'testdata/log13',
        '-f', '5-', '-c',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    with open('testdata/output13') as f:
        filecontent = f.read()
        assert 'field5:field6:field7\n' in filecontent
        assert 'field4' not in filecontent


def test_cut_fields_single():
    testargs = [
        'demeuk', '-i', 'testdata/input14', '-o', 'testdata/output14', '-l', 'testdata/log14',
        '-f', '5', '-c',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    with open('testdata/output14') as f:
        filecontent = f.read()
        assert 'field5\n' in filecontent
        assert 'field4' not in filecontent


def test_unhex():
    testargs = [
        'demeuk', '-i', 'testdata/input15', '-o', 'testdata/output15', '-l', 'testdata/log15',
        '--hex',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    with open('testdata/output15') as f:
        filecontent = f.read()
        assert 'PEÑAROL\n' in filecontent
        assert 'QWERTYUIOPÅ\n' in filecontent
        assert 'Zsófi2000\n' in filecontent
        assert 'arañas\n' in filecontent
        assert '$HEX[' not in filecontent


def test_unhtml():
    testargs = [
        'demeuk', '-i', 'testdata/input16', '-o', 'testdata/output16', '-l', 'testdata/log16',
        '--html',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    with open('testdata/output16') as f:
        filecontent = f.read()
        assert 'İSMAİL\n' in filecontent
        assert 'İSTANBUL\n' in filecontent
        assert 'şifreyok\n' in filecontent
        assert 'α\n' not in filecontent
        assert '&gt;\n' in filecontent


def test_unhtml_named():
    testargs = [
        'demeuk', '-i', 'testdata/input17', '-o', 'testdata/output17', '-l', 'testdata/log17',
        '--html', '--html-named',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    with open('testdata/output17') as f:
        filecontent = f.read()
        assert 'İSMAİL\n' in filecontent
        assert 'İSTANBUL\n' in filecontent
        assert 'şifreyok\n' in filecontent
        assert 'α\n' in filecontent
        assert '>\n' in filecontent


def test_verbose():
    testargs = [
        'demeuk', '-i', 'testdata/input18', '-o', 'testdata/output18', '-l', 'testdata/log18',
        '-f', '5-', '-c', '--verbose',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    with open('testdata/log18') as f:
        filecontent = f.read()
        assert 'Clean_cut; ' in filecontent


def test_limit():
    testargs = [
        'demeuk', '-i', 'testdata/input19', '-o', 'testdata/output19', '-l', 'testdata/log19',
        '--limit', '5',
    ]
    with patch.object(sys, 'argv', testargs):
        main()

    line_num_output = calculate_line_numbers('testdata/output19')
    assert line_num_output == 5


def test_clean_add_umlaut():
    testargs = [
        'demeuk', '-i', 'testdata/input20', '-o', 'testdata/output20', '-l', 'testdata/log20',
        '--add-umlaut', '--verbose',
    ]
    with patch.object(sys, 'argv', testargs):
        main()

    with open('testdata/output20') as f:
        filecontent = f.read()
        assert 'Eselsbrücke' in filecontent
        assert 'Fremdschämen' in filecontent
        assert 'KÄSEHOCH' in filecontent
        assert 'KA"SEHOCH' in filecontent

    testargs = [
        'demeuk', '-i', 'testdata/input20', '-o', 'testdata/output20.2', '-l', 'testdata/log20.2',
        '--umlaut', '--verbose',
    ]
    with patch.object(sys, 'argv', testargs):
        main()

    with open('testdata/output20.2') as f:
        filecontent = f.read()
        assert 'Eselsbrücke' in filecontent
        assert 'Fremdschämen' in filecontent
        assert 'KÄSEHOCH' in filecontent
        assert 'KA"SEHOCH' not in filecontent


def test_multiple_delimiters():
    testargs = [
        'demeuk', '-i', 'testdata/input21', '-o', 'testdata/output21', '-l', 'testdata/log20',
        '-c', '--verbose', '-d', ':,;,----',
    ]
    with patch.object(sys, 'argv', testargs):
        main()

    with open('testdata/output21') as f:
        filecontent = f.read()
        assert 'password\n' in filecontent
        assert 'password2\n' in filecontent
        assert 'password3\n' in filecontent
        assert 'user' not in filecontent


def test_check_email():
    testargs = [
        'demeuk', '-i', 'testdata/input22', '-o', 'testdata/output22', '-l', 'testdata/log22',
        '--verbose', '--check-email', '--remove-email',
    ]
    with patch.object(sys, 'argv', testargs):
        main()

    with open('testdata/output22') as f:
        filecontent = f.read()
        assert 'line1' in filecontent
        assert 'line2' not in filecontent
        assert 'line3' not in filecontent
        assert 'line4' not in filecontent
        assert 'line5\n' in filecontent


def test_check_hash():
    testargs = [
        'demeuk', '-i', 'testdata/input23', '-o', 'testdata/output23', '-l', 'testdata/log23',
        '--verbose', '--check-hash', '-c',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    with open('testdata/output23') as f:
        filecontent = f.read()
        assert 'baabe00a81fc405af4ab9b0f99615498' not in filecontent
        assert '$h$7/uhfibmxg83yq6y1rh5y9wjee13kh.' not in filecontent
        assert '$6$/fasjdfsadj$safjasdfasjdfa' not in filecontent
        assert '$1$Tx6cx/cA$ouWREOn7' not in filecontent
        assert 'changeme!' in filecontent
        assert 'line5' not in filecontent
        assert '12345678' in filecontent
        assert 'aaaaaa' in filecontent
        assert '$aaa$test' in filecontent
        assert '$H$8abc' in filecontent
        assert '$2a$10$bcrypt' not in filecontent
        assert '$pizza$like' in filecontent


def test_check_bug_comma_d():
    testargs = [
        'demeuk', '-i', 'testdata/input24', '-o', 'testdata/output24', '-l', 'testdata/log24',
        '--verbose', '-c', '-d', ',;:',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    with open('testdata/output24') as f:
        filecontent = f.read()
        assert 'line1' not in filecontent
        assert 'angus' in filecontent
        assert 'line2' not in filecontent
        assert 'snow' in filecontent


def test_check_non_ascii():
    testargs = [
        'demeuk', '-i', 'testdata/input25', '-o', 'testdata/output25', '-l', 'testdata/log25',
        '--verbose', '--check-non-ascii',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    with open('testdata/output25') as f:
        filecontent = f.read()
        assert 'laténight' not in filecontent
        assert 'thestrokes' in filecontent


def test_clean_non_ascii():
    testargs = [
        'demeuk', '-i', 'testdata/input26', '-o', 'testdata/output26', '-l', 'testdata/log26',
        '--verbose', '--non-ascii',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    with open('testdata/output26') as f:
        filecontent = f.read()

        assert 'polopaç' not in filecontent
        assert 'mündster' not in filecontent
        assert 'polopac' in filecontent
        assert 'mundster' in filecontent


def test_glob():
    testargs = [
        'demeuk', '-i', 'testdata/input*', '-o', 'testdata/output27', '-l', 'testdata/log27',
        '--verbose', '-c', '-d', ',;:',
    ]
    with patch.object(sys, 'argv', testargs):
        main()
    with open('testdata/output27') as f:
        assert len(f.readlines()) == 115
