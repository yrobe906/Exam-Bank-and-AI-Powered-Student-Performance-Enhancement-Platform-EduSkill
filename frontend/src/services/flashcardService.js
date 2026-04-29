import api from './api';

// Get all flashcard decks
export const getAllDecks = async () => {
  return await api.get('/api/flashcards/decks');
};

// Get a specific deck with cards
export const getDeck = async (deckId) => {
  return await api.get(`/api/flashcards/decks/${deckId}`);
};

// Get decks by subject
export const getDecksBySubject = async (subject, examBoard = null) => {
  const params = examBoard ? `?exam_board=${examBoard}` : '';
  return await api.get(`/api/flashcards/subjects/${subject}${params}`);
};

// Get all subjects
export const getAllSubjects = async () => {
  return await api.get('/api/flashcards/subjects');
};

// Get cards in a deck
export const getDeckCards = async (deckId) => {
  return await api.get(`/api/flashcards/decks/${deckId}/cards`);
};

// Get user's progress for a deck
export const getDeckProgress = async (deckId, userId) => {
  return await api.get(`/api/flashcards/decks/${deckId}/progress?user_id=${userId}`);
};

// Update card progress
export const updateCardProgress = async (cardId, userId, status) => {
  return await api.post(`/api/flashcards/cards/${cardId}/progress?user_id=${userId}&status=${status}`);
};

// Get deck statistics
export const getDeckStats = async (deckId, userId) => {
  return await api.get(`/api/flashcards/decks/${deckId}/stats?user_id=${userId}`);
};

// Get user overall statistics
export const getUserStats = async (userId) => {
  return await api.get(`/api/flashcards/user/stats?user_id=${userId}`);
};

// Create a new deck
export const createDeck = async (deckData) => {
  return await api.post('/api/flashcards/decks', deckData);
};

// Update a deck
export const updateDeck = async (deckId, deckData) => {
  return await api.put(`/api/flashcards/decks/${deckId}`, deckData);
};

// Delete a deck
export const deleteDeck = async (deckId) => {
  return await api.delete(`/api/flashcards/decks/${deckId}`);
};

// Create a flashcard
export const createFlashcard = async (cardData) => {
  return await api.post('/api/flashcards/cards', cardData);
};

// Create multiple flashcards at once
export const createFlashcardsBulk = async (cards) => {
  return await api.post('/api/flashcards/cards/bulk', cards);
};

// Update a flashcard
export const updateFlashcard = async (cardId, cardData) => {
  return await api.put(`/api/flashcards/cards/${cardId}`, cardData);
};

// Delete a flashcard
export const deleteFlashcard = async (cardId) => {
  return await api.delete(`/api/flashcards/cards/${cardId}`);
};

// Seed sample decks
export const seedSampleDecks = async () => {
  return await api.post('/api/flashcards/seed/sample-decks');
};
