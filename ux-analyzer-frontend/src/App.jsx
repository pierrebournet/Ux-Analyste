import { useState, useCallback } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert.jsx'
import { Upload, FileImage, AlertTriangle, CheckCircle, Info, Zap, Eye, Palette, Layout, Type } from 'lucide-react'
import './App.css'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      if (file.type.startsWith('image/')) {
        setSelectedFile(file)
      }
    }
  }, [])

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      if (file.type.startsWith('image/')) {
        setSelectedFile(file)
      }
    }
  }

  const convertFileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => resolve(reader.result)
      reader.onerror = error => reject(error)
    })
  }

  const analyzeImage = async () => {
    if (!selectedFile) return

    setIsAnalyzing(true)
    try {
      const base64Image = await convertFileToBase64(selectedFile)
      
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: base64Image,
          image_name: selectedFile.name
        })
      })

      const data = await response.json()
      
      if (data.success) {
        setAnalysisResult(data.analysis)
      } else {
        console.error('Erreur d\'analyse:', data.error)
      }
    } catch (error) {
      console.error('Erreur lors de l\'analyse:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return 'destructive'
      case 'medium': return 'default'
      case 'low': return 'secondary'
      default: return 'outline'
    }
  }

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'high': return <AlertTriangle className="h-4 w-4" />
      case 'medium': return <Info className="h-4 w-4" />
      case 'low': return <CheckCircle className="h-4 w-4" />
      default: return <Info className="h-4 w-4" />
    }
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'contrast': return <Eye className="h-4 w-4" />
      case 'button_size': return <Zap className="h-4 w-4" />
      case 'layout': return <Layout className="h-4 w-4" />
      case 'accessibility': return <Eye className="h-4 w-4" />
      case 'complexity': return <Layout className="h-4 w-4" />
      default: return <Info className="h-4 w-4" />
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            UX Analyzer
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Analysez l'expérience utilisateur de vos applications Power Apps et obtenez des recommandations personnalisées pour améliorer votre interface.
          </p>
        </div>

        {/* Upload Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5" />
              Télécharger une capture d'écran
            </CardTitle>
            <CardDescription>
              Glissez-déposez ou sélectionnez une image de votre application Power Apps pour commencer l'analyse.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div
              className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                dragActive 
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
                  : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              {selectedFile ? (
                <div className="space-y-4">
                  <FileImage className="h-12 w-12 mx-auto text-green-500" />
                  <div>
                    <p className="text-lg font-medium text-gray-900 dark:text-white">
                      {selectedFile.name}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                  <div className="flex gap-2 justify-center">
                    <Button onClick={analyzeImage} disabled={isAnalyzing}>
                      {isAnalyzing ? 'Analyse en cours...' : 'Analyser l\'image'}
                    </Button>
                    <Button variant="outline" onClick={() => setSelectedFile(null)}>
                      Changer d'image
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <Upload className="h-12 w-12 mx-auto text-gray-400" />
                  <div>
                    <p className="text-lg font-medium text-gray-900 dark:text-white">
                      Glissez votre image ici
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      ou cliquez pour sélectionner un fichier
                    </p>
                  </div>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="hidden"
                    id="file-upload"
                  />
                  <label htmlFor="file-upload">
                    <Button variant="outline" className="cursor-pointer">
                      Sélectionner une image
                    </Button>
                  </label>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Loading */}
        {isAnalyzing && (
          <Card className="mb-8">
            <CardContent className="pt-6">
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                  <span className="text-sm font-medium">Analyse en cours...</span>
                </div>
                <Progress value={33} className="w-full" />
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Détection des éléments UI, analyse des couleurs et génération des recommandations...
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Results */}
        {analysisResult && (
          <div className="space-y-6">
            {/* Summary */}
            <Card>
              <CardHeader>
                <CardTitle>Résumé de l'analyse</CardTitle>
                <CardDescription>
                  Analyse effectuée le {new Date(analysisResult.timestamp).toLocaleString('fr-FR')}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                      {analysisResult.recommendations?.length || 0}
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      Problèmes détectés
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-red-600 dark:text-red-400">
                      {analysisResult.recommendations?.filter(r => r.severity === 'high').length || 0}
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      Priorité haute
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                      {analysisResult.recommendations?.filter(r => r.severity === 'medium').length || 0}
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      Priorité moyenne
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                      {analysisResult.element_detection?.total_elements || 0}
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      Éléments détectés
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Detailed Results */}
            <Tabs defaultValue="recommendations" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="recommendations">Recommandations</TabsTrigger>
                <TabsTrigger value="elements">Éléments UI</TabsTrigger>
                <TabsTrigger value="colors">Couleurs</TabsTrigger>
                <TabsTrigger value="layout">Disposition</TabsTrigger>
              </TabsList>

              <TabsContent value="recommendations" className="space-y-4">
                {analysisResult.recommendations?.length > 0 ? (
                  analysisResult.recommendations.map((rec, index) => (
                    <Alert key={index} className="border-l-4 border-l-blue-500">
                      <div className="flex items-start gap-3">
                        <div className="flex items-center gap-2">
                          {getSeverityIcon(rec.severity)}
                          {getTypeIcon(rec.type)}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <AlertTitle className="text-base">{rec.title}</AlertTitle>
                            <Badge variant={getSeverityColor(rec.severity)}>
                              {rec.severity}
                            </Badge>
                          </div>
                          <AlertDescription className="space-y-2">
                            <p>{rec.description}</p>
                            <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-md">
                              <p className="font-medium text-sm text-blue-800 dark:text-blue-200">
                                💡 Suggestion:
                              </p>
                              <p className="text-sm text-blue-700 dark:text-blue-300">
                                {rec.suggestion}
                              </p>
                            </div>
                            <div className="bg-green-50 dark:bg-green-900/20 p-3 rounded-md">
                              <p className="font-medium text-sm text-green-800 dark:text-green-200">
                                🔧 Correctif:
                              </p>
                              <p className="text-sm text-green-700 dark:text-green-300">
                                {rec.fix}
                              </p>
                            </div>
                          </AlertDescription>
                        </div>
                      </div>
                    </Alert>
                  ))
                ) : (
                  <Alert>
                    <CheckCircle className="h-4 w-4" />
                    <AlertTitle>Excellente UX !</AlertTitle>
                    <AlertDescription>
                      Aucun problème majeur détecté dans votre interface. Votre application respecte les bonnes pratiques UX.
                    </AlertDescription>
                  </Alert>
                )}
              </TabsContent>

              <TabsContent value="elements" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Layout className="h-5 w-5" />
                      Éléments détectés
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        Total: {analysisResult.element_detection?.total_elements || 0} éléments
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {analysisResult.element_detection?.elements?.slice(0, 6).map((element, index) => (
                          <div key={index} className="border rounded-lg p-3">
                            <div className="flex items-center justify-between mb-2">
                              <Badge variant="outline">{element.type}</Badge>
                              <span className="text-xs text-gray-500">
                                {element.dimensions.width}×{element.dimensions.height}px
                              </span>
                            </div>
                            <div className="text-xs text-gray-600 dark:text-gray-400">
                              Position: ({element.position.x}, {element.position.y})
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="colors" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Palette className="h-5 w-5" />
                      Analyse des couleurs
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <div className="text-sm font-medium mb-2">Score de contraste</div>
                        <div className="flex items-center gap-2">
                          <Progress 
                            value={Math.min((analysisResult.color_analysis?.contrast_score || 0) / 100 * 100, 100)} 
                            className="flex-1" 
                          />
                          <span className="text-sm">
                            {(analysisResult.color_analysis?.contrast_score || 0).toFixed(1)}
                          </span>
                        </div>
                      </div>
                      <div>
                        <div className="text-sm font-medium mb-2">Couleurs dominantes</div>
                        <div className="flex flex-wrap gap-2">
                          {analysisResult.color_analysis?.dominant_colors?.slice(0, 8).map((color, index) => (
                            <div
                              key={index}
                              className="w-8 h-8 rounded border border-gray-300"
                              style={{ backgroundColor: `rgb(${color[0]}, ${color[1]}, ${color[2]})` }}
                              title={`RGB(${color[0]}, ${color[1]}, ${color[2]})`}
                            />
                          ))}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="layout" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Layout className="h-5 w-5" />
                      Analyse de la disposition
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <div className="text-sm font-medium mb-2">Densité globale</div>
                        <Progress 
                          value={(analysisResult.layout_analysis?.overall_density || 0) * 100} 
                          className="w-full" 
                        />
                        <div className="text-xs text-gray-500 mt-1">
                          {((analysisResult.layout_analysis?.overall_density || 0) * 100).toFixed(1)}% de l'écran utilisé
                        </div>
                      </div>
                      <div>
                        <div className="text-sm font-medium mb-2">Répartition par zones</div>
                        <div className="grid grid-cols-3 gap-2 text-xs">
                          {Object.entries(analysisResult.layout_analysis?.zone_densities || {}).map(([zone, density]) => (
                            <div key={zone} className="text-center">
                              <div className="font-medium capitalize">{zone}</div>
                              <div className="text-gray-500">{(density * 100).toFixed(1)}%</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

