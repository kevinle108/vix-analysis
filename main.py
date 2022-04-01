import analysis as analysis
def main():
  actions = {
    '1' : 'View & analyze historical closing values of VIX & VFIAX',
    '2' : 'View & analyze YTD gain/loss of VIX & VFIAX',
    '3' : 'View YTD gain/loss of VIX (inverse) & VFIAX',
    '4' : 'Exit Program',
  }
  
  while True:
    print('\nVIX Analysis Menu:\n')
    for keypress, description in actions.items():
      print(f'[{keypress}] - {description}')
    selection = input("""\nSelect an option:  """)
    if selection in actions:
      if selection == '1':
        analysis.show_historical()
      elif selection == '2':
        analysis.show_recent(use_inverse = False, show_analysis=True)
      elif selection == '3':
        analysis.show_recent(use_inverse = True, show_analysis=False)
      else: break 
    else:
      print('Invalid Selection!')
  return

if __name__ == '__main__':
  main()