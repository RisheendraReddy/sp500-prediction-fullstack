import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const healthCheck = async () => {
  const response = await api.get('/api/v1/health')
  return response.data
}

export const listModels = async () => {
  const response = await api.get('/api/v1/models')
  return response.data
}

export const trainModel = async (modelType, valSize = 0.2) => {
  const response = await api.post('/api/v1/train', {
    model_type: modelType,
    val_size: valSize,
    save_model: true,
  })
  return response.data
}

export const predictSingle = async (dateId, features, modelType = null) => {
  const params = modelType ? { model_type: modelType } : {}
  const response = await api.post('/api/v1/predict', {
    date_id: dateId,
    features: features,
  }, { params })
  return response.data
}

export const predictBatch = async (predictions, modelType = null) => {
  const params = modelType ? { model_type: modelType } : {}
  const response = await api.post('/api/v1/predict/batch', {
    predictions: predictions,
  }, { params })
  return response.data
}

export const predictFromFile = async (file, modelType = null) => {
  const formData = new FormData()
  formData.append('file', file)
  if (modelType) {
    formData.append('model_type', modelType)
  }
  const response = await api.post('/api/v1/predict/file', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    responseType: 'blob',
  })
  return response.data
}

export default api

