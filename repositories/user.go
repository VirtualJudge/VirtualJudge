package repositories

import (
	"VirtualJudge/models"
	"errors"
	"sync"
)

type Query func(user models.User) bool

type UserRepository interface {
	Exec(query Query, action Query, limit int, mode int) (ok bool)
	Select(query Query) (user models.User, found bool)
	SelectMany(query Query, limit int) (results []models.User)

	InsertOrUpdate(user models.User) (updateUser models.User, err error)
	Delete(query Query, limit int) (deleted bool)
}

type UserMemoryRepository struct {
	source map[int64]models.User
	mu     sync.RWMutex
}

const (
	// ReadOnlyMode will RLock(read) the data .
	ReadOnlyMode = iota
	// ReadWriteMode will Lock(read/write) the data.
	ReadWriteMode
)

func (r *UserMemoryRepository) Exec(query Query, action Query, limit int, mode int) (ok bool) {
	loops := 0

	if mode == ReadOnlyMode {
		r.mu.RLock()
		defer r.mu.RUnlock()
	} else {
		r.mu.Lock()
		defer r.mu.Unlock()
	}

	for _, movie := range r.source {
		ok = query(movie)
		if ok {
			if action(movie) {
				loops++
				if limit >= loops {
					break // break
				}
			}
		}
	}
	return
}

func (r *UserMemoryRepository) Select(query Query) (user models.User, found bool) {
	found = r.Exec(query, func(m models.User) bool {
		user = m
		return true
	}, 1, ReadOnlyMode)
	if !found {
		user = models.User{}
	}

	return
}

func (r *UserMemoryRepository) SelectMany(query Query, limit int) (results []models.User) {
	r.Exec(query, func(m models.User) bool {
		results = append(results, m)
		return true
	}, limit, ReadOnlyMode)

	return

}

func (r *UserMemoryRepository) InsertOrUpdate(user models.User) (updateUser models.User, err error) {
	id := user.Id

	if id == 0 { // 创建一个新的操作
		var lastID int64
		// 找到最大的ID，避免重复。
		// 在实际使用时您可以使用第三方库去生成
		// 一个string类型的UUID
		r.mu.RLock()
		for _, item := range r.source {
			if item.Id > lastID {
				lastID = item.Id
			}
		}
		r.mu.RUnlock()

		id = lastID + 1
		user.Id = id

		// map-specific thing
		r.mu.Lock()
		r.source[id] = user
		r.mu.Unlock()

		return user, nil
	}

	// 更新操作是基于movie.ID的，
	// 在例子中我们允许了对poster和genre的更新（如果它们非空）。
	// 当然我们可以只是做单纯的数据替换操作:
	// r.source[id] = movie
	// 并注释掉下面的代码;
	current, exists := r.Select(func(m models.User) bool {
		return m.Id == id
	})

	if !exists { // 当ID不存在时抛出一个error
		return models.User{}, errors.New("failed to update a nonexistent movie")
	}

	// map-specific thing
	r.mu.Lock()
	r.source[id] = current
	r.mu.Unlock()

	return user, nil
}

func (r *UserMemoryRepository) Delete(query Query, limit int) (deleted bool) {
	return r.Exec(query, func(m models.User) bool {
		delete(r.source, m.Id)
		return true
	}, limit, ReadWriteMode)
}
