import request from './request'

// 资源相关API
export const getResources = () => {
  return request.get('/resources')
}

export const createResource = (data) => {
  return request.post('/resources', data)
}

export const updateResource = (id, data) => {
  return request.put(`/resources/${id}`, data)
}

export const deleteResource = (id) => {
  return request.delete(`/resources/${id}`)
}

// 报价相关API
export const getQuotations = () => {
  return request.get('/quotations')
}

export const getQuotationById = (id) => {
  return request.get(`/quotations/${id}`)
}

export const createQuotation = (data) => {
  return request.post('/quotations', data)
}

export const updateQuotation = (id, data) => {
  return request.put(`/quotations/${id}`, data)
}

export const deleteQuotation = (id) => {
  return request.delete(`/quotations/${id}`)
}

// 项目相关API
export const getProjects = () => {
  return request.get('/projects')
}

export const getProject = (id) => {
  return request.get(`/projects/${id}`)
}

export const getProjectById = getProject

export const createProject = (data) => {
  return request.post('/projects', data)
}

export const updateProject = (id, data) => {
  return request.put(`/projects/${id}`, data)
}

export const deleteProject = (id) => {
  return request.delete(`/projects/${id}`)
}
