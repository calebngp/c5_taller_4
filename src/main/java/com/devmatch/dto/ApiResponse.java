package com.devmatch.dto;

/**
 * Modelo genérico para las respuestas de la API REST
 * Proporciona una estructura consistente para todas las respuestas
 * 
 * @param <T> Tipo de datos contenidos en la respuesta
 */
public class ApiResponse<T> {
    
    private String message;
    private int code;
    private T data;
    private boolean success;
    
    // Constructors
    public ApiResponse() {}
    
    public ApiResponse(String message, int code, T data, boolean success) {
        this.message = message;
        this.code = code;
        this.data = data;
        this.success = success;
    }
    
    // Static factory methods para respuestas comunes
    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>("Operación exitosa", 200, data, true);
    }
    
    public static <T> ApiResponse<T> success(String message, T data) {
        return new ApiResponse<>(message, 200, data, true);
    }
    
    public static <T> ApiResponse<T> created(T data) {
        return new ApiResponse<>("Recurso creado exitosamente", 201, data, true);
    }
    
    public static <T> ApiResponse<T> noContent(String message) {
        return new ApiResponse<>(message, 204, null, true);
    }
    
    public static <T> ApiResponse<T> error(String message, int code) {
        return new ApiResponse<>(message, code, null, false);
    }
    
    public static <T> ApiResponse<T> notFound(String message) {
        return new ApiResponse<>(message, 404, null, false);
    }
    
    public static <T> ApiResponse<T> badRequest(String message) {
        return new ApiResponse<>(message, 400, null, false);
    }
    
    // Getters and Setters
    public String getMessage() {
        return message;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
    
    public int getCode() {
        return code;
    }
    
    public void setCode(int code) {
        this.code = code;
    }
    
    public T getData() {
        return data;
    }
    
    public void setData(T data) {
        this.data = data;
    }
    
    public boolean isSuccess() {
        return success;
    }
    
    public void setSuccess(boolean success) {
        this.success = success;
    }
    
    @Override
    public String toString() {
        return "ApiResponse{" +
                "message='" + message + '\'' +
                ", code=" + code +
                ", success=" + success +
                ", data=" + data +
                '}';
    }
}
