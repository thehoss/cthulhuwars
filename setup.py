from distutils.core import setup

setup(
    name='cthulhuwars',
    version='0.1dev',
    author='MountainsOfMadness',
    author_email='masterblasterofdisaster@gmail.com',
    packages=['cthulhuwars'],
    entry_points={
        'cw_board.games': 'cthulhuwars = cthulhuwars.board:Board',
        'cw_board.players': 'cthulhuwars.cw_mcts = cthulhuwars.mcts:MonteCarlo',
    },
    license='LICENSE',
    description="An implementation of Cthulhu Wars.",
)
