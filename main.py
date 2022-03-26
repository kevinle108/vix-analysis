import analysis as analysis
def main():

  actions = {
    '1' : 'View Historical Trends of VIX and Total Market',
    '2' : 'View Recent Gain/Loss w/ VIX',
    '3' : 'View Recent Gain/Loss w/ VIX inverse',
    '4' : 'Exit Program',
    't' : 'historical gain-loss'
  }
  
  while True:
    print('\nVIX Analysis Menu:\n')
    for keypress, description in actions.items():
      print(f'\t{keypress} - {description}')
    selection = input("""\nSelect an option:  """)
    if selection in actions:
      if selection == '1':
        analysis.show_historical()
      elif selection == '2':
        analysis.show_recent(use_inverse = False)
      elif selection == '3':
        analysis.show_recent(use_inverse = True)
      elif selection == 't':
        analysis.historical_gain_loss()
      else: break 
    else:
      print('Invalid Selection!')
  return

if __name__ == '__main__':
  main()