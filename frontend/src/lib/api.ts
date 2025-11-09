import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Event {
  id: number;
  slug: string;
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  registration_deadline: string;
  base_fee: number;
  is_active: boolean;
}

export interface StudentRegistration {
  first_name: string;
  last_name: string;
  email: string;
  mobile: string;
  grade: string;
  age: number;
  stream?: string;
  school_name: string;
  city: string;
  state: string;
  coupon_code?: string;
}

export interface SchoolRegistration {
  school_name: string;
  contact_person: string;
  email: string;
  mobile: string;
  city: string;
  state: string;
  num_students: number;
}

export const eventApi = {
  getBySlug: async (slug: string): Promise<Event> => {
    const response = await api.get(`/events/${slug}`);
    return response.data;
  },

  registerStudent: async (eventId: number, data: StudentRegistration) => {
    const response = await api.post(`/registrations/student`, {
      event_id: eventId,
      ...data,
    });
    return response.data;
  },

  registerSchool: async (eventId: number, data: SchoolRegistration) => {
    const response = await api.post(`/registrations/school`, {
      event_id: eventId,
      ...data,
    });
    return response.data;
  },
};

export default api;
