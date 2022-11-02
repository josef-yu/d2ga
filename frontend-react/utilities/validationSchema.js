import * as yup from 'yup';

const DEFAULT_NOT_EMPTY_ERROR = 'Field must not be empty';

export const LoginSchema = yup.object({
    username: yup.string().required(DEFAULT_NOT_EMPTY_ERROR),
    password: yup.string().required(DEFAULT_NOT_EMPTY_ERROR),
})