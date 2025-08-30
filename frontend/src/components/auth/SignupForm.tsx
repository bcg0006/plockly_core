import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Paper,
  InputAdornment,
  IconButton,
  FormControl,
  InputLabel,
  OutlinedInput,
  FormHelperText,
} from '@mui/material';
import { Visibility, VisibilityOff, Email, Lock } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

interface SignupFormData {
  email: string;
  password: string;
  password_confirm: string;
}

interface SignupFormErrors {
  email?: string;
  password?: string;
  password_confirm?: string;
  non_field_errors?: string;
}

const SignupForm: React.FC = () => {
  const navigate = useNavigate();
  const { signup } = useAuth();
  const [formData, setFormData] = useState<SignupFormData>({
    email: '',
    password: '',
    password_confirm: '',
  });

  const [errors, setErrors] = useState<SignupFormErrors>({});
  const [showPassword, setShowPassword] = useState(false);
  const [showPasswordConfirm, setShowPasswordConfirm] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [generalError, setGeneralError] = useState('');

  // Password strength indicators
  const getPasswordStrength = (password: string): { score: number; label: string; color: string } => {
    let score = 0;
    if (password.length >= 8) score++;
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;

    const strengthMap = [
      { label: 'Very Weak', color: '#ff1744' },
      { label: 'Weak', color: '#ff9100' },
      { label: 'Fair', color: '#ffc400' },
      { label: 'Good', color: '#00c853' },
      { label: 'Strong', color: '#00e676' },
    ];

    return {
      score: Math.min(score, 5),
      ...strengthMap[Math.min(score - 1, 4)],
    };
  };

  const passwordStrength = getPasswordStrength(formData.password);

  const validateForm = (): boolean => {
    const newErrors: SignupFormErrors = {};

    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters long';
    } else if (passwordStrength.score < 3) {
      newErrors.password = 'Password is too weak. Include uppercase, lowercase, numbers, and symbols.';
    }

    // Password confirmation validation
    if (!formData.password_confirm) {
      newErrors.password_confirm = 'Please confirm your password';
    } else if (formData.password !== formData.password_confirm) {
      newErrors.password_confirm = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (field: keyof SignupFormData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.value;
    setFormData(prev => ({ ...prev, [field]: value }));

    // Clear field-specific error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }

    // Clear general errors
    if (generalError) {
      setGeneralError('');
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setGeneralError('');
    setSuccessMessage('');

    try {
      const success = await signup(formData.email, formData.password, formData.password_confirm);

      if (success) {
        setSuccessMessage('Account created successfully! Redirecting to dashboard...');

        // Redirect to dashboard after a short delay
        setTimeout(() => {
          navigate('/dashboard');
        }, 2000);
      } else {
        setGeneralError('Signup failed. Please try again.');
      }
    } catch (error: any) {
      // Handle validation errors from backend
      if (error.email || error.password || error.password_confirm || error.non_field_errors) {
        setErrors(error);
      } else {
        setGeneralError('An error occurred during signup. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleTogglePasswordVisibility = (field: 'password' | 'password_confirm') => {
    if (field === 'password') {
      setShowPassword(!showPassword);
    } else {
      setShowPasswordConfirm(!showPasswordConfirm);
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        padding: 2,
        backgroundColor: 'grey.50',
      }}
    >
      <Paper
        elevation={3}
        sx={{
          padding: 4,
          width: '100%',
          maxWidth: 400,
          borderRadius: 2,
        }}
      >
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Create Account
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Join Plockly v2 and start building amazing things!
          </Typography>
        </Box>

        <form onSubmit={handleSubmit}>
          {/* Email Field */}
          <TextField
            fullWidth
            label="Email Address"
            type="email"
            value={formData.email}
            onChange={handleInputChange('email')}
            error={!!errors.email}
            helperText={errors.email}
            margin="normal"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Email color="action" />
                </InputAdornment>
              ),
            }}
            disabled={isLoading}
          />

          {/* Password Field */}
          <FormControl fullWidth margin="normal" error={!!errors.password}>
            <InputLabel htmlFor="password-input">Password</InputLabel>
            <OutlinedInput
              id="password-input"
              type={showPassword ? 'text' : 'password'}
              value={formData.password}
              onChange={handleInputChange('password')}
              startAdornment={
                <InputAdornment position="start">
                  <Lock color="action" />
                </InputAdornment>
              }
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    onClick={() => handleTogglePasswordVisibility('password')}
                    edge="end"
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              }
              label="Password"
              disabled={isLoading}
            />
            <FormHelperText>
              {errors.password || (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Typography variant="caption">Strength:</Typography>
                  <Box
                    sx={{
                      width: 60,
                      height: 8,
                      backgroundColor: 'grey.200',
                      borderRadius: 1,
                      overflow: 'hidden',
                    }}
                  >
                    <Box
                      sx={{
                        width: `${(passwordStrength.score / 5) * 100}%`,
                        height: '100%',
                        backgroundColor: passwordStrength.color,
                        transition: 'width 0.3s ease',
                      }}
                    />
                  </Box>
                  <Typography
                    variant="caption"
                    sx={{ color: passwordStrength.color, fontWeight: 'bold' }}
                  >
                    {passwordStrength.label}
                  </Typography>
                </Box>
              )}
            </FormHelperText>
          </FormControl>

          {/* Password Confirmation Field */}
          <FormControl fullWidth margin="normal" error={!!errors.password_confirm}>
            <InputLabel htmlFor="password-confirm-input">Confirm Password</InputLabel>
            <OutlinedInput
              id="password-confirm-input"
              type={showPasswordConfirm ? 'text' : 'password'}
              value={formData.password_confirm}
              onChange={handleInputChange('password_confirm')}
              startAdornment={
                <InputAdornment position="start">
                  <Lock color="action" />
                </InputAdornment>
              }
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    onClick={() => handleTogglePasswordVisibility('password_confirm')}
                    edge="end"
                  >
                    {showPasswordConfirm ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              }
              label="Confirm Password"
              disabled={isLoading}
            />
            {errors.password_confirm && (
              <FormHelperText>{errors.password_confirm}</FormHelperText>
            )}
          </FormControl>

          {/* General Errors */}
          {errors.non_field_errors && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {errors.non_field_errors}
            </Alert>
          )}

          {/* Network/Server Errors */}
          {generalError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {generalError}
            </Alert>
          )}

          {/* Success Message */}
          {successMessage && (
            <Alert severity="success" sx={{ mt: 2 }}>
              {successMessage}
            </Alert>
          )}

          {/* Submit Button */}
          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="large"
            disabled={isLoading}
            sx={{ mt: 3, mb: 2, py: 1.5 }}
          >
            {isLoading ? (
              <CircularProgress size={24} color="inherit" />
            ) : (
              'Create Account'
            )}
          </Button>

          {/* Login Link */}
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Already have an account?{' '}
              <Button
                variant="text"
                color="primary"
                onClick={() => navigate('/login')}
                disabled={isLoading}
                sx={{ textTransform: 'none' }}
              >
                Sign in here
              </Button>
            </Typography>
          </Box>
        </form>
      </Paper>
    </Box>
  );
};

export default SignupForm;
