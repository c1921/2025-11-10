export const getStatusColor = (value: number, reverse: boolean = false): string => {
  if (reverse) {
    // 对于心情，值越高越好
    if (value > 70) return 'success'
    if (value > 40) return 'warning'
    return 'error'
  } else {
    // 对于疲劳和饥饿，值越低越好
    if (value < 30) return 'success'
    if (value < 60) return 'warning'
    return 'error'
  }
}

export const getStatusColorHex = (value: number, reverse: boolean = false): string => {
  if (reverse) {
    if (value > 70) return '#4caf50'
    if (value > 40) return '#ff9800'
    return '#f44336'
  } else {
    if (value < 30) return '#4caf50'
    if (value < 60) return '#ff9800'
    return '#f44336'
  }
}
