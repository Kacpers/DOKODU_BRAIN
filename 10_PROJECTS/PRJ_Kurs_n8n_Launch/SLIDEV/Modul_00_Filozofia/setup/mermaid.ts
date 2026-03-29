import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => ({
  theme: 'base',
  themeVariables: {
    primaryColor: '#1E2D40',
    primaryTextColor: '#A8D8EA',
    primaryBorderColor: '#E63946',
    lineColor: '#E63946',
    secondaryColor: '#0F2137',
    tertiaryColor: '#0A1628',
    edgeLabelBackground: '#0F2137',
    fontFamily: 'Inter, sans-serif',
    fontSize: '14px',
    actorBkg: '#0F2137',
    actorBorder: '#E63946',
    actorTextColor: '#ffffff',
    signalColor: '#A8D8EA',
    signalTextColor: '#A8D8EA',
    noteBkgColor: '#1E2D40',
    noteTextColor: '#A8D8EA',
  }
}))
